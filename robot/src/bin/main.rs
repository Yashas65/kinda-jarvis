#![no_std]
#![no_main]
#![deny(
    clippy::mem_forget,
    reason = "mem::forget is generally not safe to do with esp_hal types, especially those \
    holding buffers for the duration of a data transfer."
)]
#![deny(clippy::large_stack_frames)]

use embassy_executor::Spawner;
use embassy_time::{Duration, Timer};
use esp_hal::clock::CpuClock;
use esp_hal::timer::timg::TimerGroup;
use log::info;
use esp_hal::{
    Async,
    uart::{
        Config, Uart
    }
};


use robot::uart_comm;

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! {
    loop {}
}

// This creates a default app-descriptor required by the esp-idf bootloader.
// For more information see: <https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/app_image_format.html#application-description>
esp_bootloader_esp_idf::esp_app_desc!();

#[allow(
    clippy::large_stack_frames,
    reason = "it's not unusual to allocate larger buffers etc. in main"
)]

#[embassy_executor::task]
async fn uart_task(mut uart: Uart<'static, Async>) {
    let mut buf = [0u8; 64];
    loop {
        match uart.read_async(&mut buf).await {
            Ok(n) => {
                let msg = core::str::from_utf8(&buf[..n]).unwrap_or("??");
                uart_comm::handle_message(msg);
                info!("Received: {}", msg);
                // TODO: parse commands here
            }
            Err(e) => {
                info!("UART error: {:?}", e);
            }
        }
    }
}

#[esp_rtos::main]
async fn main(spawner: Spawner) -> ! {
    // generator version: 1.2.0

    esp_println::logger::init_logger_from_env();

    let config = esp_hal::Config::default().with_cpu_clock(CpuClock::max());
    let peripherals = esp_hal::init(config);

    let timg0 = TimerGroup::new(peripherals.TIMG0);
    esp_rtos::start(timg0.timer0);

    info!("Embassy initialized!");
    info!("Optimus online.");

    // UART1: GPIO4 = TX, GPIO5 = RX (wires to laptop USB-serial adapter)
    let uart = Uart::new(peripherals.UART0, Config::default())
    .unwrap()
    .into_async();
    
    spawner.spawn(uart_task(uart)).unwrap();

    loop {
        info!("Optimus alive.");
        Timer::after(Duration::from_secs(5)).await;
    }

    // for inspiration have a look at the examples at https://github.com/esp-rs/esp-hal/tree/esp-hal-v1.0.0/examples
}
// this file handles te parsing of the raw string recieved from the python side and 
// matches the req. function
// the syntax must be defined on the python side 

use log::info;



fn set_servo_angle(command:&str){
    let mut data = command.split(":");
    let _ = data.next(); // the command which by which the string is already seperated
    let location = data.next();
    let value = data.next();
    info!("got to move {}",location.unwrap_or("unknown"));
    info!("with value {}", value.unwrap_or("unknown"));
}
fn manage_gestures(command:&str){

}
fn pose(command:&str){

}

pub fn handle_message(message:&str){  //breaks the big line chunk into smaller chunks of commands
    for command in message.split(";"){
        match &command[0..3]{
            "set" =>set_servo_angle(command)  ,                //set servo angle
            "ges" =>manage_gestures(command)  ,                 // gesture
            "pos" =>pose(command),                               // poses like look straight
            _=>info!("invalid command!!!")
        }
    }
}
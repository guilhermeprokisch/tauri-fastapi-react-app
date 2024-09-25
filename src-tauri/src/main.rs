use std::process::Command as StdCommand;
use std::sync::Mutex;
use tauri::api::process::{Command, CommandChild, CommandEvent};
use tauri::{Manager, State, WindowEvent};

struct APIManagerState {
    child: Mutex<Option<CommandChild>>,
}

#[tauri::command]
async fn start_server(state: State<'_, APIManagerState>) -> Result<String, String> {
    let mut child_lock = state
        .child
        .lock()
        .map_err(|e| format!("Failed to lock mutex: {}", e))?;

    if child_lock.is_some() {
        println!("API server is already running");
        return Ok("API server is already running".into());
    }

    println!("Attempting to start API server...");

    let (mut rx, child) = Command::new_sidecar("api")
        .expect("failed to create `api` binary command")
        .spawn()
        .map_err(|e| format!("Failed to spawn API server: {}", e))?;

    println!("API server process spawned successfully");

    tauri::async_runtime::spawn(async move {
        println!("Starting to listen for API server events");
        while let Some(event) = rx.recv().await {
            match event {
                CommandEvent::Stdout(line) => println!("API: {}", line),
                CommandEvent::Stderr(line) => eprintln!("API Error: {}", line),
                CommandEvent::Error(error) => eprintln!("API Process Error: {}", error),
                CommandEvent::Terminated(status) => {
                    println!("API Process Terminated with status: {:?}", status)
                }
                _ => {}
            }
        }
        println!("Stopped listening for API server events");
    });

    *child_lock = Some(child);
    println!("API server started successfully");
    Ok("API server started successfully".into())
}

#[tauri::command]
async fn stop_server(state: State<'_, APIManagerState>) -> Result<String, String> {
    let mut child_lock = state
        .child
        .lock()
        .map_err(|e| format!("Failed to lock mutex: {}", e))?;

    if let Some(child) = child_lock.take() {
        println!("Attempting to stop API server");

        // Get the process ID
        let pid = child.pid();

        // On Unix-like systems (macOS, Linux)
        #[cfg(unix)]
        {
            // Use pkill to terminate all child processes
            if let Err(e) = StdCommand::new("pkill")
                .args(&["-P", &pid.to_string()])
                .output()
            {
                eprintln!("Failed to terminate child processes: {}", e);
            }
        }

        // On Windows
        #[cfg(windows)]
        {
            // Use taskkill to terminate the process tree
            if let Err(e) = StdCommand::new("taskkill")
                .args(&["/F", "/T", "/PID", &pid.to_string()])
                .output()
            {
                eprintln!("Failed to terminate process tree: {}", e);
            }
        }

        // Now kill the main process
        match child.kill() {
            Ok(_) => {
                println!("API server stopped successfully");
                Ok("API server stopped successfully".into())
            }
            Err(e) => {
                eprintln!("Failed to stop API server: {}", e);
                Err(format!("Failed to stop API server: {}", e))
            }
        }
    } else {
        println!("API server is not running");
        Ok("API server is not running".into())
    }
}

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

fn main() {
    tauri::Builder::default()
        .manage(APIManagerState {
            child: Mutex::new(None),
        })
        .setup(|app| {
            let app_handle = app.handle();
            tauri::async_runtime::spawn(async move {
                let state = app_handle.state::<APIManagerState>();
                match start_server(state).await {
                    Ok(msg) => println!("{}", msg),
                    Err(e) => eprintln!("Failed to start API server: {}", e),
                }
            });
            Ok(())
        })
        .on_window_event(|event| {
            if let WindowEvent::Destroyed = event.event() {
                let state = event.window().state::<APIManagerState>();
                tauri::async_runtime::block_on(async {
                    match stop_server(state).await {
                        Ok(msg) => println!("{}", msg),
                        Err(e) => eprintln!("Error stopping API server: {}", e),
                    }
                });
            }
        })
        .invoke_handler(tauri::generate_handler![greet, start_server, stop_server])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

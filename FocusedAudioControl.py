import keyboard
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import time
import win32gui
import win32process

incr = 0.025
time_step = 0.05

while True:
    time.sleep(time_step)
    
    hwnd = win32gui.GetForegroundWindow()

    if hwnd != 0:
        if not "ApplicationFrameWindow" in win32gui.GetClassName(hwnd):
            pid = win32process.GetWindowThreadProcessId(hwnd)

            sessions = AudioUtilities.GetAllSessions()
            audio_session_ids = []
            
            for session in sessions:
                current_session = session.Process and session.Process.pid
                audio_session_ids.append(current_session)
                
            if pid[1] in audio_session_ids:
                session_index = audio_session_ids.index(pid[1])
                volume_interface = sessions[session_index]._ctl.QueryInterface(ISimpleAudioVolume)

                if keyboard.is_pressed('ctrl+alt+subtract'):
                    if volume_interface.GetMasterVolume() - incr >= 0:
                        volume_interface.SetMasterVolume(volume_interface.GetMasterVolume() - incr, None)
                    elif volume_interface.GetMasterVolume() - incr <= 0:
                        volume_interface.SetMasterVolume(0, None)
                    
                if keyboard.is_pressed('ctrl+alt+plus'):
                    if volume_interface.GetMasterVolume() + incr <= 1:
                        volume_interface.SetMasterVolume(volume_interface.GetMasterVolume() + incr, None)
                    elif volume_interface.GetMasterVolume() + incr >= 1:
                        volume_interface.SetMasterVolume(1, None)
            else:
                pass
        else:
            pass
    else:
        pass
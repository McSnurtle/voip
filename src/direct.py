"""WARNING: THIS SCRIPT IS A TESTING HODGE-PODGE AND NOT MEANT FOR PRODUCTION. DO NOT USE IT UNLESS YOU KNOW WHAT YOU ARE DOING OR MC_SNURTLE GOT EXTREMELY LAZY AND TOLD YOU TO USE THIS ANYWAY."""
# imports - direct.py, by Mc_Snurtle
import threading

import client
import server


# ========== Functions ==========
def validate_ip(address: str, port: int | str) -> bool:
    if isinstance(port, str):
        port = int(port)

    if port > 65535:
        raise ValueError("Port exceeds 65535")

    if "." in address:
        if len(address.split(".")) != 4:
            raise IndexError("Address must be IPv4. i.e. `127.0.0.1`.")

    return True


def client_mainloop():
    while RUNNING:
        client_socket.send_audio(recorder.buffer.get())


if __name__ == "__main__":
    RUNNING: bool = True
    address, port = "127.0.0.1", 20000
    target = input(":: Enter your target server IPv4 address along with its port [127.0.0.1:20000] ")
    if ":" in target:
        target_split = target.split(":", 1)
        if validate_ip(*target_split):
            address, port = target_split

    server_socket = server.Server()
    client_socket = client.Client(destination=(address, int(port)))
    recorder = client.Recorder()

    server_thread = threading.Thread(target=server_socket.mainloop, daemon=True)
    # client_thread = threading.Thread(target=client_mainloop, daemon=True)
    server_thread.start()
    # client_thread.start()
    # run client in main thread to keepalive
    client_mainloop()

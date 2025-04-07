import speedtest
import math

def test_internet_speed():
    print("Initializing Speed Test...")
    try:
        st = speedtest.Speedtest()

        print("Finding the best server based on ping...")
        st.get_best_server()

        print("Performing download test...")
        download_speed_bps = st.download()

        print("Performing upload test...")
        upload_speed_bps = st.upload()

        ping_ms = st.results.ping

        download_speed_mbps = download_speed_bps / 1_000_000
        upload_speed_mbps = upload_speed_bps / 1_000_000

        print("\n--- Internet Speed Test Results ---")
        print(f"Ping: {ping_ms:.2f} ms")
        print(f"Download Speed: {download_speed_mbps:.2f} Mbps")
        print(f"Upload Speed: {upload_speed_mbps:.2f} Mbps")
        print("-----------------------------------")

    except speedtest.SpeedtestException as e:
        print(f"An error occurred during the speed test: {e}")
    except ImportError:
        print("Error: The 'speedtest-cli' library is not installed.")
        print("Please install it using: pip install speedtest-cli")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_internet_speed()
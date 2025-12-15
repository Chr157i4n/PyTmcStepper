"""
Upload TMC driver files to Raspberry Pi Pico

Requirements:
    pip install mpremote

Usage:
    python upload_to_pico.py [COM_PORT]

Example:
    python upload_to_pico.py COM3
    python upload_to_pico.py /dev/ttyACM0
"""

import subprocess
import sys
import os

# Default COM port
DEFAULT_PORT = "COM4"  # Windows
# DEFAULT_PORT = "/dev/ttyACM0"  # Linux
# DEFAULT_PORT = "/dev/tty.usbmodem*"  # macOS

# Base path (script location)
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def run_mpremote(port, *args, show_output=False):
    """Run mpremote command"""
    cmd = ["python", "-m", "mpremote", "connect", port] + list(args)
    # print(f"  > {' '.join(args)}")

    if show_output:
        # Run with live output (for 'run' command)
        result = subprocess.run(cmd)
        return result.returncode == 0
    else:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.returncode != 0 and "exists" not in result.stderr.lower():
            print(f"    Warning: {result.stderr.strip()}")
            return False
        return True


def main():
    port = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PORT

    print("=" * 60)
    print(f"Uploading TMC driver to Pico on {port}")
    print("=" * 60)

    # Check if mpremote is installed
    try:
        subprocess.run(["python", "-m", "mpremote", "--help"], capture_output=True, check=True)
    except FileNotFoundError:
        print("Error: mpremote not installed!")
        print("Install with: pip install mpremote")
        sys.exit(1)

    # MicroPython compatibility modules (go to /lib/)
    micropython_modules = [
        "src/tmc_driver/micropython/enum.py",
        "src/tmc_driver/micropython/logging.py",
        "src/tmc_driver/micropython/types.py",
        "src/tmc_driver/micropython/typing.py",
        "src/tmc_driver/micropython/threading.py",
    ]

    # TMC driver core files
    tmc_driver_files = [
        "src/tmc_driver/_tmc_logger.py",
        "src/tmc_driver/_tmc_gpio_board.py",
        "src/tmc_driver/_tmc_math.py",
        "src/tmc_driver/_tmc_exceptions.py",
        "src/tmc_driver/_tmc_stepperdriver.py",
        "src/tmc_driver/_tmc_stallguard.py",
        "src/tmc_driver/tmc_2240.py",
    ]

    # Communication modules
    tmc_com_files = [
        "src/tmc_driver/com/_tmc_com.py",
        "src/tmc_driver/com/_tmc_com_spi_base.py",
        "src/tmc_driver/com/_tmc_com_spi_micropython.py",
    ]

    # Register modules
    tmc_reg_files = [
        "src/tmc_driver/reg/_tmc_reg.py",
        "src/tmc_driver/reg/_tmc224x_reg.py",
    ]

    # Motion control modules
    tmc_mc_files = [
        "src/tmc_driver/motion_control/_tmc_mc.py",
        "src/tmc_driver/motion_control/_tmc_mc_step_dir.py",
        "src/tmc_driver/motion_control/_tmc_mc_step_pwm_dir.py",
        "src/tmc_driver/motion_control/_tmc_mc_step_reg.py",
        "src/tmc_driver/motion_control/_tmc_mc_vactual.py",
    ]

    # Enable control modules
    tmc_ec_files = [
        "src/tmc_driver/enable_control/_tmc_ec.py",
        "src/tmc_driver/enable_control/_tmc_ec_pin.py",
        "src/tmc_driver/enable_control/_tmc_ec_toff.py",
    ]

    # main file
    main_file = "demo_pico_move.py"

    # Directories to create on Pico
    directories = [
        "lib",
        "lib/tmc_driver",
        "lib/tmc_driver/com",
        "lib/tmc_driver/reg",
        "lib/tmc_driver/motion_control",
        "lib/tmc_driver/enable_control",
    ]

    # Step 1: Create directories
    print("\n[1/5] Creating directories on Pico...")
    for dir_path in directories:
        run_mpremote(port, "fs", "mkdir", dir_path)

    # Step 2: Upload MicroPython compatibility modules to /lib/
    print("\n[2/5] Uploading MicroPython compatibility modules...")
    for src in micropython_modules:
        src_path = os.path.join(BASE_PATH, src)
        if os.path.exists(src_path):
            filename = os.path.basename(src)
            dst = f":lib/{filename}"
            run_mpremote(port, "fs", "cp", src_path, dst)
        else:
            print(f"    SKIP: {src} (not found)")

    # Step 3: Upload TMC driver files
    print("\n[3/5] Uploading TMC driver files...")
    all_tmc_files = tmc_driver_files + tmc_com_files + tmc_reg_files + tmc_mc_files + tmc_ec_files

    for src in all_tmc_files:
        src_path = os.path.join(BASE_PATH, src)
        if os.path.exists(src_path):
            # Convert src/tmc_driver/... to lib/tmc_driver/...
            dst = src.replace("src/", ":lib/")
            run_mpremote(port, "fs", "cp", src_path, dst)
        else:
            print(f"    SKIP: {src} (not found)")

    # Step 4: Upload demo file
    print("\n[4/5] Uploading demo script...")
    src_path = os.path.join(BASE_PATH, main_file)
    if os.path.exists(src_path):
        run_mpremote(port, "fs", "cp", src_path, f":{main_file}")
    else:
        print(f"    SKIP: {main_file} (not found)")

    # print("\n" + "=" * 60)
    # print("Upload complete!")
    # print("=" * 60)
    # print("\n[5/5] Running main file...")
    # run_mpremote(port, "run", main_file, show_output=True)


if __name__ == "__main__":
    main()

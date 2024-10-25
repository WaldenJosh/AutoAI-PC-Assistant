import subprocess
import tempfile
import os
import time

class PowerShellExecutor:
    def __init__(self):
        """
        Initialize a persistent PowerShell session using subprocess.
        """
        self.process = subprocess.Popen(
            ["powershell", "-NoExit", "-Command", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

    def run_command(self, command):
        """
        Send a command to the PowerShell session and capture the output.
        """
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()

        # Use communicate to capture the output and error (if any)
        stdout, stderr = self.process.communicate(timeout=5)

        if stderr:
            return f"Error: {stderr.strip()}"
        return stdout.strip()

    def run_admin_command(self, command):
        """
        Run a PowerShell command with elevated privileges and capture the output.
        """
        try:
            # Create a temporary file for the output
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
                temp_file_path = temp_file.name

            # PowerShell script that outputs to a temporary file
            powershell_script = f"""
            $output = {command}
            $output | Out-File -FilePath "{temp_file_path}" -Encoding UTF8
            """
            
            # Run the script with admin privileges using Start-Process
            subprocess.run(
                ["powershell", "-Command", f'Start-Process powershell -ArgumentList \'-Command "{powershell_script}"\' -Verb RunAs'],
                check=True
            )

            # Allow time for the elevated process to complete
            time.sleep(3)  # Increase this if commands take longer to execute

            # Retry until the file is ready
            for _ in range(10):
                if os.path.exists(temp_file_path):
                    break
                time.sleep(0.5)

            # Read the output from the temporary file
            if os.path.exists(temp_file_path):
                with open(temp_file_path, "r") as file:
                    output = file.read()

                # Clean up the temporary file
                os.remove(temp_file_path)

                return output.strip()
            else:
                return "Error: Could not retrieve output from admin command."
                
        except Exception as e:
            return f"Failed to execute command as admin: {e}"

    def close(self):
        """
        Close the PowerShell session gracefully, if still active.
        """
        try:
            if self.process and self.process.stdin:
                self.process.stdin.write("exit\n")
                self.process.stdin.flush()
            self.process.terminate()
            self.process.wait()
        except Exception as e:
            print(f"Error closing PowerShell session: {e}")

# Example Usage
if __name__ == "__main__":
    ps_executor = PowerShellExecutor()
    
    # Run a regular command
    output = ps_executor.run_command("Get-Date")
    print("Output of Get-Date:", output)

    # Run an admin command
    admin_output = ps_executor.run_admin_command("Get-Process")
    print("Output of Get-Process with admin privileges:", admin_output)
    
    # Close the session
    ps_executor.close()

import subprocess
import time

class PowerShellExecutor:
    def __init__(self):
        """
        Initialize a persistent PowerShell session using subprocess.
        """
        # Start PowerShell process with pipes for stdin, stdout, and stderr
        self.process = subprocess.Popen(
            ["powershell", "-NoExit", "-Command", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # To handle strings directly without byte encoding
            bufsize=1   # Line-buffered for real-time output
        )
        # Buffer to store output
        self.output_buffer = []

    def run_command(self, command):
        """
        Send a command to the PowerShell session.

        Parameters:
        command (str): PowerShell command to be executed.

        Returns:
        None
        """
        # Write the command to the PowerShell process stdin
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()

        # Allow some time for command to execute
        time.sleep(0.1)  # Adjust as needed for responsiveness

        # Read output until end of stream
        self.output_buffer = []
        while True:
            output_line = self.process.stdout.readline()
            if not output_line or output_line.strip() == "":
                break
            self.output_buffer.append(output_line.strip())

    def get_result(self):
        """
        Retrieve the result from the last executed command.

        Returns:
        str: Output of the last command
        """
        return "\n".join(self.output_buffer)

    def close(self):
        """
        Close the PowerShell session gracefully.
        """
        self.process.stdin.write("exit\n")
        self.process.stdin.flush()
        self.process.terminate()
        self.process.wait()

# Example Usage
if __name__ == "__main__":
    # Create a PowerShell session
    ps_executor = PowerShellExecutor()
    
    # Run a command
    ps_executor.run_command("Get-Date")
    
    # Retrieve and print the output
    output = ps_executor.get_result()
    print("Output of Get-Date:", output)
    
    # Run another command
    ps_executor.run_command("$x = 42; Write-Output $x")
    output = ps_executor.get_result()
    print("Output of variable assignment:", output)
    
    # Close the PowerShell session
    ps_executor.close()

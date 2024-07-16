"""Core modules for the project."""

from typing import Union, Any
from pathlib import Path
from dataclasses import dataclass


@dataclass
class PopenArgs:
    """Dataclass for Popen arguments."""

    args: str | list[Union[str, bytes, Path]]

    def __post_init__(self):
        if isinstance(self.args, str):
            self.args = self.args.split()

    @property
    def command(self):
        return " ".join(self.args)

    def to_list(self):
        return self.args


class SubprocessRun:
    """Define a subprocess to run."""

    def __init__(
        self,
        args: PopenArgs,
        input=None,
        capture_output=False,
        timeout=None,
        check=False,
        stream_ouput=False,
        **kwargs,
    ):
        self.args: PopenArgs = args
        self.input: str | bytes | None = input
        self.capture_output: bool | Any = capture_output
        self.timeout: int | None = timeout
        self.check: bool = check
        self.stream_output: bool = stream_ouput
        self.kwargs = kwargs

    def run(self):
        """Run the subprocess."""
        import subprocess

        print(f"Running: {self.args.command}")
        try:
            if self.stream_output:
                result = subprocess.run(
                    self.args.to_list(),
                    input=self.input,
                    capture_output=self.capture_output,
                    timeout=self.timeout,
                    text=True,
                    check=self.check,
                    **self.kwargs,
                )
            else:
                result = subprocess.run(
                    self.args.to_list(),
                    input=self.input,
                    capture_output=self.capture_output,
                    timeout=self.timeout,
                    check=self.check,
                    **self.kwargs,
                )
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            raise e

import subprocess
import tempfile
import sys


class ChromePDF(object):

    _chrome_options = [
        '--headless',
        '--disable-gpu',
        '--no-margins',
    ]

    def __init__(self, chrome_exec, sandbox=True):
        """
        Constructor
        chrome_exec (string) - path to chrome executable
        """

        assert isinstance(chrome_exec, str) and chrome_exec != ''

        self._chrome_exe = chrome_exec
        self._sandbox = sandbox

    def html_to_pdf(self, html_byte_string, output_file, raise_exception=False):
        """
        Converts the given html_byte_string to PDF stored at output_file

        html_byte_string (string) - html to be rendered to PDF
        output_file (File object) - file object to output PDF file

        returns True if successful and False otherwise
        """

        assert isinstance(html_byte_string, str)

        with tempfile.NamedTemporaryFile(suffix='.html') as html_file:

            html_file.write(str.encode(html_byte_string))
            html_file.flush()

            temp_file_url = 'file://{0}'.format(html_file.name)

            pdf = self.create_pdf(temp_file_url, output_file, raise_exception=False)
            if not pdf:
                return False

        return True

    def page_to_pdf(self, url, output_file, raise_exception=False):
        """
        Converts the given html_byte_string to PDF stored at output_file

        html_byte_string (string) - html to be rendered to PDF
        output_file (File object) - file object to output PDF file

        returns True if successful and False otherwise
        """
        pdf = self.create_pdf(url, output_file, raise_exception)
        if not pdf:
            return False

        return True

    def create_pdf(self, url, output_file, raise_exception):
        print_to_pdf_command = self.generate_shell_command(
            self._chrome_exe, url, output_file.name, self._sandbox,
        )

        isNotWindows = not sys.platform.startswith('win32')

        try:
            subprocess.run(print_to_pdf_command, shell=isNotWindows, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            if raise_exception:
                raise
            return False

        return True

    def generate_shell_command(self, chrome_exe, input_url, output_file_name, sandbox):
        """
        Generate the command string

        chrome_exe (string) - path to chrome executable
        input_url (string) - html to be rendered to PDF
        output_file_name (string) - file object to output PDF file
        sandbox (boolean) - using sandbox mode

        returns command string
        """

        args = ['{chrome_exec}'] + self._chrome_options

        if not sandbox:
            args += ['--no-sandbox']

        args += ['--print-to-pdf="{output_file}"', '{input_url}']

        return ' '.join(args).format(
            chrome_exec=chrome_exe,
            input_url=input_url,
            output_file=str(output_file_name),
        )

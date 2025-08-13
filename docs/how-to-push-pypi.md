
### Submitting to PyPI

Submitting your project to the Python Package Index (PyPI) allows anyone to install it using `pip`. Since you're using Poetry, the process is quite streamlined.

1.  **Create a PyPI Account:** If you don't already have one, register on [pypi.org](https://pypi.org).
    
2.  **Generate an API Token:** On your PyPI account page, go to "Account settings" and create a new API token. Make sure to copy it immediately, as you won't be able to see it again.
    
3.  **Configure Poetry:** Tell Poetry about your token so it can authenticate with PyPI. Run this command in your terminal, replacing `<your-pypi-api-token>` with the token you just copied:
    
    ```bash
    poetry config pypi-token.pypi <your-pypi-api-token>
    ```
    
4.  **Build Your Project:** This command packages your application into the standard distribution formats.
    
    ```bash
    poetry build
    ```
    
5.  **Publish:** Finally, this command uploads your package to PyPI.

    ```bash
    poetry publish
    ```
    

Once these steps are complete, your `gfr` tool will be publicly available, and anyone can install it by running `pip install gfr`.
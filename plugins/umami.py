from datasette import hookimpl


@hookimpl
def extra_body_script():
    return {
        "script": '</script><script async defer data-website-id="e2972688-f31b-4e36-ad7a-85d5bd4ec253" src="https://analytics.oakland.works/civic.js">'
    }

# stipendium
Web application for managing a large quantity of stipends for multiple related organizations.

## Roadmap

This is a work in progress and the current configuration of the application will
definitely change as the project progresses. Right now there is no way to login,
work can be saved, but no data is protected. Storage is on the server and there
is no way to store the data somewhere else like Amazon S3 or Google Drive or any
other server.

## Goals

- Every action must take less then 100ms.
- User interface must be as simple as possible. No extra clutter.
- Responsive. Equal funtionality across devices.

## Development

Run the application for testing:

```bash
flask --app stipendium.py --debug run
```

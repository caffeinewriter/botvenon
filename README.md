# Botvenon

A simple welcomebot for Mastodon instances.

## Usage

Requires Python3 and pip.

Run `pip install -r requirements.txt`.

See the included `.env.sample` file for information on configuration.

To work effectively, the account this bot is running on *must* be a default follow on your instance. 

Docker support is in progress.

To use the docker version, build it, and run it with:

```sh
docker build -t botvenon .
docker run --mount source=data-volume,target=/data -it botvenon:latest
```
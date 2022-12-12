[![Join the chat at https://t.me/joinchat/ABFVWBE0AhkyyhREoaboXQ](https://img.shields.io/badge/Telegram-Group-orange?style=flat&logo=telegram)](https://t.me/joinchat/ABFVWBE0AhkyyhREoaboXQ) &nbsp;&nbsp;[![Join the chat at https://discord.gg/tYgADKx](https://img.shields.io/discord/719186998686122046?style=flat&label=Discord&logo=discord)](https://discord.gg/tYgADKx)

Centrifugo is an open-source scalable real-time messaging server. Centrifugo can instantly deliver messages to application online users connected over supported transports (WebSocket, HTTP-streaming, SSE/EventSource, GRPC, SockJS, WebTransport). Centrifugo has the concept of a channel – so it's a user-facing PUB/SUB server.

Centrifugo is language-agnostic and can be used to build chat apps, live comments, multiplayer games, real-time data visualizations, collaborative tools, etc. in combination with any backend. It is well suited for modern architectures and allows decoupling the business logic from the real-time transport layer.

Several official client SDKs for browser and mobile development wrap the bidirectional protocol. In addition, Centrifugo supports a unidirectional approach for simple use cases with no SDK dependency.

For details, go to the [Centrifugo documentation site](https://centrifugal.dev).

![scheme](https://raw.githubusercontent.com/centrifugal/centrifugo/v2/docs/content/images/scheme_sketch.png)

### How to install

See [installation instructions](https://centrifugal.dev/docs/getting-started/installation) in Centrifugo documentation.

### Highlights

* Centrifugo is fast and capable to scale to millions of simultaneous connections
* Simple integration with any application – Centrifugo works as a separate service, provides HTTP and GRPC API
* Client real-time SDKs for popular frontend environments – for both web and mobile development
* Strict client protocol based on Protobuf schema, with JSON and binary data transfer support
* Bidirectional transport support (WebSocket and SockJS) for full-featured communication
* Unidirectional transport support for simple use cases with zero SDK dependency - use native APIs (SSE, Fetch, WebSocket, GRPC)
* User authentication with JWT or over connection request proxy to the configured HTTP/GRPC endpoint
* Proper connection management and expiration control
* Various types of channel subscriptions: client-side or server-side
* Transform RPC calls sent over real-time transport to the configured HTTP or GRPC endpoint calls
* Presence information for channels (show all active clients in a channel)
* History information for channels (last messages published into a channel)
* Join/leave events for channels (client subscribed/unsubscribed)
* Automatic recovery of missed messages between reconnects over configured retention period
* Built-in administrative web panel
* Cross-platform – works on Linux, macOS and Windows
* Ready to deploy (Docker, RPM/DEB packages, automatic TLS certificates, Prometheus instrumentation, Grafana dashboard)
* Open-source license

### Backing

This repository is hosted by [packagecloud.io](https://packagecloud.io/).

<a href="https://packagecloud.io/"><img height="46" width="158" alt="Private NPM registry and Maven, RPM, DEB, PyPi and RubyGem Repository · packagecloud" src="https://packagecloud.io/images/packagecloud-badge.png" /></a>

Also thanks to [JetBrains](https://www.jetbrains.com/) for supporting OSS (most of the code here written in Goland):

<a href="https://www.jetbrains.com/"><img height="140" src="https://resources.jetbrains.com/storage/products/company/brand/logos/jb_beam.png" alt="JetBrains logo"></a>

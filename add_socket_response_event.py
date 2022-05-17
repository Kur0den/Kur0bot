from discord.gateway import DiscordWebSocket, utils, _log, KeepAliveHandler, ReconnectWebSocket

async def received_message(self, msg, /):
    if type(msg) is bytes:
        self._buffer.extend(msg)

        if len(msg) < 4 or msg[-4:] != b'\x00\x00\xff\xff':
            return
        msg = self._zlib.decompress(self._buffer)
        msg = msg.decode('utf-8')
        self._buffer = bytearray()

    self.log_receive(msg)
    msg = utils._from_json(msg)

    _log.debug('For Shard ID %s: WebSocket Event: %s', self.shard_id, msg)


    # add dispatch
    self._dispatch('socket_response', msg)


    event = msg.get('t')
    if event:
        self._dispatch('socket_event_type', event)

    op = msg.get('op')
    data = msg.get('d')
    seq = msg.get('s')
    if seq is not None:
        self.sequence = seq

    if self._keep_alive:
        self._keep_alive.tick()

    if op != self.DISPATCH:
        if op == self.RECONNECT:
            # "reconnect" can only be handled by the Client
            # so we terminate our connection and raise an
            # internal exception signalling to reconnect.
            _log.debug('Received RECONNECT opcode.')
            await self.close()
            raise ReconnectWebSocket(self.shard_id)

        if op == self.HEARTBEAT_ACK:
            if self._keep_alive:
                self._keep_alive.ack()
            return

        if op == self.HEARTBEAT:
            if self._keep_alive:
                beat = self._keep_alive.get_payload()
                await self.send_as_json(beat)
            return

        if op == self.HELLO:
            interval = data['heartbeat_interval'] / 1000.0
            self._keep_alive = KeepAliveHandler(ws=self, interval=interval, shard_id=self.shard_id)
            # send a heartbeat immediately
            await self.send_as_json(self._keep_alive.get_payload())
            self._keep_alive.start()
            return

        if op == self.INVALIDATE_SESSION:
            if data is True:
                await self.close()
                raise ReconnectWebSocket(self.shard_id)

            self.sequence = None
            self.session_id = None
            _log.info('Shard ID %s session has been invalidated.', self.shard_id)
            await self.close(code=1000)
            raise ReconnectWebSocket(self.shard_id, resume=False)

        _log.warning('Unknown OP code %s.', op)
        return

    if event == 'READY':
        self._trace = trace = data.get('_trace', [])
        self.sequence = msg['s']
        self.session_id = data['session_id']
        # pass back shard ID to ready handler
        data['__shard_id__'] = self.shard_id
        _log.info('Shard ID %s has connected to Gateway: %s (Session ID: %s).',
                 self.shard_id, ', '.join(trace), self.session_id)

    elif event == 'RESUMED':
        self._trace = trace = data.get('_trace', [])
        # pass back the shard ID to the resumed handler
        data['__shard_id__'] = self.shard_id
        _log.info('Shard ID %s has successfully RESUMED session %s under trace %s.',
                 self.shard_id, self.session_id, ', '.join(trace))

    try:
        func = self._discord_parsers[event]
    except KeyError:
        _log.debug('Unknown event %s.', event)
    else:
        func(data)

    # remove the dispatched listeners
    removed = []
    for index, entry in enumerate(self._dispatch_listeners):
        if entry.event != event:
            continue

        future = entry.future
        if future.cancelled():
            removed.append(index)
            continue

        try:
            valid = entry.predicate(data)
        except Exception as exc:
            future.set_exception(exc)
            removed.append(index)
        else:
            if valid:
                ret = data if entry.result is None else entry.result(data)
                future.set_result(ret)
                removed.append(index)

    for index in reversed(removed):
        del self._dispatch_listeners[index]


DiscordWebSocket.received_message = received_message

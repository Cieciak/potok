import zjadacz
from zjadacz import byte

potok_segment_name_parser = zjadacz.sequenceOf(
    byte.word(b'-'),
    byte.regex(b'[A-Z]+'),
    byte.word(b'-'),
    byte.newl(),
).map(
    lambda s: s.result[1]
)

potok_begin_segment_parser = zjadacz.sequenceOf(
    byte.regex(b'[A-Z]+'),
    byte.newl(),
    byte.regex(b'[0-9]\\.[0-9]'),
    byte.newl(),
    byte.regex(b'[A-Z]+'),
    byte.newl(),
).map(
    lambda s: {
        'name': s.result[0].decode('utf-8'),
        'version': s.result[2].decode('utf-8'),
        'method': s.result[4].decode('utf-8'),
    }
)

potok_tag_parser = zjadacz.sequenceOf(
    byte.regex(b'[A-Za-z]+').map(lambda s: s.result.decode('utf-8')),
    byte.word(b': '),
    byte.regex(b'[A-Za-z0-9/]+'),
    byte.newl(),
).map(
    lambda s: {s.result[0]: s.result[2]}
)

potok_head_segment_parser = zjadacz.many(
    potok_tag_parser,
)

potok_body_segment_parser = byte.regex(b'.*')

potok_segment_parser = potok_segment_name_parser.match({
    b'INIT': potok_begin_segment_parser,
    b'HEAD': potok_head_segment_parser,
    b'BODY': potok_body_segment_parser,
})

potok_message_parser = zjadacz.sequenceOf(
    potok_segment_parser,
    potok_segment_parser,
    potok_segment_parser,
)
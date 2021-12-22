from grpc.tools import protoc
protoc.main(
    (
        '',
        '-I.',
        '--python_out=../my_if',
        '--grpc_python_out=../my_if',
        'my_if.proto',
    )
)
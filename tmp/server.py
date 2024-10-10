import socket
import os
import sys

def start_server(port, directory):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(1)
    print(f"서버가 포트 {port}에서 시작되었습니다.")
    print(f"파일을 제공하는 디렉터리: {os.path.abspath(directory)}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"클라이언트 연결: {addr}")
        
        request = client_socket.recv(1024)  # 바이트로 요청 받기
        print(f"요청(바이트): {request}")

        try:
            request = request.decode('utf-8')
            print(f"요청: {request}")

            parts = request.split()

            # 요청이 유효한지 확인
            if len(parts) > 1:
                filename = parts[1][1:]  # 슬래시 제거
                if filename == '':
                    filename = 'index.html'
            else:
                filename = 'index.html'  # 기본 파일 설정

            filepath = os.path.join(directory, filename)

            with open(filepath, 'rb') as f:
                response_body = f.read()
                
            # 수정된 응답 생성
            response = 'HTTP/1.0 200 OK\r\n\r\n'.encode() + response_body

        except FileNotFoundError:
            response = 'HTTP/1.0 404 NOT FOUND\r\n\r\n<h1>404 Not Found</h1>'.encode()

        except UnicodeDecodeError:
            print("요청 해석 중 오류 발생.")
            response = 'HTTP/1.0 400 BAD REQUEST\r\n\r\n<h1>400 Bad Request</h1>'.encode()

        # 클라이언트에 응답 전송
        client_socket.sendall(response)
        
        # 연결 닫기
        client_socket.close()  # 비지속형 연결 구현

if __name__ == "__main__":
    port = 8000
    directory = "."

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    if len(sys.argv) > 2:
        directory = sys.argv[2]

    start_server(port, directory)

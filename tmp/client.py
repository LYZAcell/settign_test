import sys
import socket
import os

def main():
    # 명령줄 인수 처리
    if len(sys.argv) != 4:
        print("Usage: ./client.py <IP> <PORT> <FILENAME>")
        sys.exit(1)

    ip_address = sys.argv[1]
    port = int(sys.argv[2])
    filename = sys.argv[3]

    # 파일 존재 여부 확인
    if not os.path.isfile(filename):
        print(f"파일이 존재하지 않습니다: {filename}")
        sys.exit(1)

    # 소켓 생성
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((ip_address, port))
            print(f"서버에 연결됨: {ip_address}:{port}")

            # HTTP GET 요청 구성
            request = f"GET /{filename} HTTP/1.1\r\nHost: {ip_address}\r\nConnection: close\r\n\r\n"
            client_socket.send(request.encode())
            print(f"요청 전송: {request.strip()}")

            # 서버로부터 응답 받기
            response = b""
            while True:
                part = client_socket.recv(4096)
                if not part:
                    break
                response += part
            
            # 응답 출력 및 본문 처리
            response_decoded = response.decode('utf-8')
            print("응답 수신:")
            print(response_decoded)

            # 응답에서 본문 저장
            handle_response(response_decoded, filename)

        except ConnectionRefusedError:
            print("서버에 연결할 수 없습니다. 서버가 실행되고 있는지 확인하세요.")
        except Exception as e:
            print(f"오류 발생: {e}")

def handle_response(response_decoded, filename):
    # 응답에서 파일 저장
    if "200 OK" in response_decoded:
        if "\r\n\r\n" in response_decoded:
            header, body = response_decoded.split("\r\n\r\n", 1)
            print("헤더 부분:")
            print(header)

            # 파일명 수정: filename + "1"
            file_name_base, file_extension = os.path.splitext(filename)
            new_filename = f"{file_name_base}+1{file_extension}"

            with open(new_filename, 'w', encoding='utf-8') as f:
                f.write(body)
            print(f"파일 저장됨: {new_filename}")

        else:
            print("서버 응답에 본문이 없음.")
    elif "404 Not Found" in response_decoded:
        print("요청한 파일을 찾을 수 없습니다.")
    else:
        print("파일을 가져오는 데 실패했습니다.")

if __name__ == "__main__":
    main()

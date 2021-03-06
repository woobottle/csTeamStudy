# 컴퓨터 네트워크 정리

## 패킷 스위칭

End ponit 시스템들은 서로 메시지를 교환한다.

메시지에는 제어기능(연결 설정), email, jpeg, mp3 등 같은 데이터를 포함한다.

긴 메시지를 패킷이라고 하는 작은 데이터 덩어리로 분할한다.

패킷은 링크의 최대 전송 속도와 같은 속도로 각각의 통신 링크상에서 전송된다.

패킷 스위치가 R bits / sec의 속도로 링크상에서 L bits의 패킷을 송신한다면 그 패킷을 전송하는 데 걸리는 시간은 L / R 초이다.(시간 = 거리 / 속도)

### Store-and-forward

대부분의 패킷 스위치가 이용하는 방식

저장-후-전달은 스위치가 출력 링크로 패킷의 첫 비트를 전송하기 전에 전체 패킷을 받아야함을 의미한다.

패킷의 비트를 먼저 저장한 후(store)한 후, 라우터가 패킷의 모든 비트를 수신한 후에만 출력 링크로 그 패킷을 전송(forward)하기 시작함, 즉 라우터는 패킷 하나를 완전히 받기 전까지 출력링크로 보내지 않고 완전히 받고보낸다.

하나의 패킷이 N개의 링크를 통해(각 링크는 R의 전송속도) 전달되는 데 걸리는 총 종단 간 지연은 N * L / R (L은 패킷 하나의 크기)

### 큐잉 지연

출력 큐(출력 버퍼)는 각 링크에 대해 패킷 스위치가 전달할 패킷을 저장해 놓는 공간

도착하는 패킷은 특정한 출력 링크로 나가야하는데 그 링크가 다른 패킷을 전송하고 있다면, 도착하는 패킷은 출력버퍼에서 대기해야한다. 이것을 큐잉 지연이라고 한다.

큐잉 지연은 가변적이고 네트워크의 혼잡정도에 따라 달라진다.

이 큐가 가득차있는데 어떤 패킷이 들어가려고 하면 패킷 손실이 발생한다. 정책에 따라 다르겠지만 새로 도착하는 패킷을 버릴 수도 있고, 기존에 큐에 대기중인 패킷을 버릴 수도 있다.

이런 경우는 네트워크 경로 상에서 각 링크의 전달 속도차이가 심할 때 자주 발생한다. (A - 100Mbps 링크 - 라우터 - 15Mbps 링크 - B)

### 전달 테이블과 라우팅 프로토콜

라우터의 출력 링크 결정은 어떻게 이루어지는가?

인터넷에서 모든 end point들은 ip주소라고 하는 고유의 주소를 갖는다. 소느느 패킷의 헤더에 목적지의 ip주소를 포함시킨다.(ip주소는 계층적 구조를 갖는다.)

라우터는 패킷의 목적지 주소의 일부를 조사하고 그 패킷을 이웃 라우터로 전달한다. 

각 라우터는 목적지 주소를 라우터의 출력 링크로 맵핑하는 전달 테이블(forwarding table)을 갖고있다.

라우터는 올바른 출력 링크를 찾기 위해 주소를 조사하고 이 목적지 주소를 이용하여 전달 테이블을 검색한다.

주변 라우터에 물어봐서 계속해서 찾아가는 방식

전달테이블은 여러 특별한 라우팅 프로토콜을 이용하여 만들어진다. 라우팅 프로토콜은 각 라우터로부터 각 목적지까지의 최단 경로를 결정하고 라우터에 전달 테이블을 설정하는 데 이 최단 경로 결과를 이용한다.

## OSI 7 layer(Open System Interconnection)

계층구조는 크고 복잡한 시스템의 잘 정의된 특정 부분을 논의할 수 있게해준다.

시스템이 계층 구조를 갖는다면, 특정 계층이 제공하는 서비스의 구현을 변경하는 것도 쉽다

한 계층이 변한다고해도 다른 계층에는 영향을 미치지 않는다.

한 계층이 상위 계층에 제공하는 서비스에 관심을 갖고, 이것을 계층의 서비스 모델이라고 한다. 서비스의 수행작용이 방향성을 갖는다.

프로토콜 계층은 소프트웨어, 하드웨어 또는 둘의 통합으로 구현할 수 있다.

HTTP, SMTP같은 application layer 프로토콜은 대부분 종단 시스템의 소프트웨어로 구현된다.

TCP, UDP와 같은 transport layer 프로토콜또한 마찬가지로 소프트웨어로 구현된다.

IP와 같은 network layer는 종종 하드웨어와 소프트웨어의 혼합구현이다.

링크, 물리 계층은 특정 링크상에 통신을 다루는 책임이 있으므로 전형적으로 부여된 링크와 관련된 네트워크 인터페이스 카드로 구현된다.(이더넷이나 wifi 인터페이스 카드)

각 네트워크 구성요소에는 하나의 n 계층 프로토콜이 있다.

계층화의 잠재된 결점은 한 계층의 기능이 하위 계층과 기능적으로 중복된다는 것이다.

많은 프로토콜 스택이 링크와 종단 시스템 두 곳 모두에서 오류복구 기능을 제공한다.

어느 한 계층에서의 기능이 다른 계층에만 존재하는 정보롤 필요로 할 수 있다는 것이다.(ex timestamp)

다양한 계층의 프로토콜을 모두 합하여 프로토콜 스택(protocol stack)이라고 한다.

인터넷 프로토콜 스택은 5개 계층으로 구성된다.(애플리케이션 / 트랜스포트 / 네트워크 / 링크 / 물리)

## ![스크린샷 2021-12-13 02 10 27](https://user-images.githubusercontent.com/48282185/145722181-68d95353-8687-4b72-bfe2-a2112328df43.png)

+ application layer
  + 사용자의 어플리케이션이 네트워크에 접근할 수 있도록 해준다.
  + 사용자를 위한 인터페이스를 지원
  + 응용 프로세스 간의 정보 교환을 담당(한 컴퓨터내에서의 두 프로세스 혹은 다른 엔드포인트의 두 프로세스)
  + 어플리케이션 계층에서의 패킷은 메시지라고 불린다
  + 대표적으로 http, ftp, smtp가 있다.
+ presentation layer
  + 데이터를 어떻게 표현할지 정하는 역할(인코딩 / 디코딩)
  + 애플리케이션들이 교환하는 데이터의 의미를 해석하도록 하는 서비스를 제공
  + 데이터가 표현 / 저장되는 포멧을 걱정하지 않아도 되게 해준다
  + 데이터 압축, 암호화와 복호화를 포함한다.
+ session layer
  + 통신 장치 간 상호작용 및 동기화를 제공(연결 상태를 만들어준다.)
  + 연결 세션에서의 데이터 교환과 에러 발생 시의 복구를 관리
  + 체킹포인트와 회복방법을 세우는 수단을 포함한다.
+ transport layer
  + 신뢰성있고 정확한 데이터 전송을 담당
  + 송신자와 수신자 간의 신뢰적, 효율적 데이터 전송을 위해 오류검출 및 복구, 흐름제어와 중복검사, 혼잡제어 등을 수행
  + 트랜스포트 계층에서의 패킷은 세그먼트(header + payload(상위 계층 데이터 = message))라고 불린다.
  + 대표적으로 tcp(연결지향형), udp가 있다.
+ network layer(a.k.a IP 계층)
  + 라우팅 기능을 맡고 있는 계층으로 목적지까지 가장 안전하고 빠르게 데이터를 보내는 기능을 수행(최적의 경로 설정 가능)
  + 트랜스 포트 계층프로토콜의 세크먼트와 목적지 주소를 네트워크를 전달하면 datagram으로 만들어 목적지까지 전달함
  + 데이터 그램이 이동하는 경로를 설정하는 라우팅 프로토콜을 포함한다
+ Data-link layer
  + 물리적인 연결을 통하여 인접한 두 장치 간의 신뢰성 있는 정보 전송을 담당(transport의 신뢰성 보장 기능과는 다름)
  + 오류발생 시 재전송하는 기능이 존재(CRC - 오류순환검사)
  + Mac 주소를 이용한 통신
  + 데이터 계층의 패킷은 frame으로 불린다.
+ physical layer
  + 전기적, 기계적, 기능적인 특성을 이용해 데이터를 전송
  + 케이블, 리피터, 허브등의 장비가 사용됨
  + 비트 단위

[참고링크1](https://velog.io/@cgotjh/%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC-OSI-7-%EA%B3%84%EC%B8%B5-OSI-7-LAYER-%EA%B8%B0%EB%B3%B8-%EA%B0%9C%EB%85%90-%EA%B0%81-%EA%B3%84%EC%B8%B5-%EC%84%A4%EB%AA%85)

[참고링크2](https://shlee0882.tistory.com/110)

### 캡슐화

애플리케이션 계층의 메시지(payload) + header = segment

트랜스포트 계층의 세그먼트(payload) + header = datagram

네트워크 계층의 데이터그램(payload) + header = frame



## 보안

+ 스니핑
  + 스니퍼(네트워크상에 흘러 다니는 트래픽을 엿보는 도청장치)를 이용하여 데이터를 도청하는 행위를 말한다.
  + 일반적으로 작동하는 IP 주소 필터링과 MAC 주소 필터링을 수행하지 않고, 랜카드로 들어오는 전기 신호를 모두 읽어 들여 다른 이의 패킷을 관찰하여 정보를 유출시키는 것
  + 이더넷은 로컬네트워크 내의 모든 호스트가 같은 선을 공유하는 데 이를 악의적으로 노린 것이다.
  + ping이용한 스니퍼 탐지가 있다.
+ 스푸핑
  + 외부 악의적 네트워크 침입자가 임의로 웹사이트를 구성하여 일반 사용자들의 방문을 유도해 인터넷 프로토콜인 TCP/IP의 구조적 결함을 이용하여 사용자의 시스템 권한을 획득한 뒤 정보를 빼가는 해킹 방법이다. 
  + 스푸핑 공격의 종류에는 ARP 스푸핑, IP 스푸핑, DNS 스푸핑, 이메일 스푸핑 등이 존재한다
+ DoS(Denial of Service)
  + 시스템을 악의적으로 공격해 해당 시스템의 [리소스](https://ko.wikipedia.org/wiki/리소스)를 부족하게 하여 원래 의도된 용도로 사용하지 못하게 하는 공격이다.[[1\]](https://ko.wikipedia.org/wiki/서비스_거부_공격#cite_note-1) 대량의 [데이터 패킷](https://ko.wikipedia.org/w/index.php?title=데이터_패킷&action=edit&redlink=1)을 통신망으로 보내고 특정 [서버](https://ko.wikipedia.org/wiki/서버)에 수많은 접속 시도를 하는 등 다른 이용자가 정상적으로 서비스 이용을 하지 못하게 하거나, 서버의 [TCP](https://ko.wikipedia.org/wiki/전송_제어_프로토콜) 연결을 바닥내는 등의 공격이 이 범위에 포함된다

[참고 링크](https://copycode.tistory.com/65)



## Web과 HTTP

애플리케이션 프로토콜인 HTTP는 웹의 중심이다

http는 클라이언트와 서버 두 가지 프로그램으로 구현된다. 이 두 프로그램의 통신을 http라는 프로토콜을 이용하여 수행하게된다.

http는 메시지를 어떻게 교환하는지에 대해 정의하고있다.

웹 페이지(문서)는 객체들로 구성되는데 객체는 단순히 단일 URL로 지정할 수 있는 하나의 파일이다.

대부분의 웹페이지는 기본 HTML파일과 여러 참조 객체로 구성된다.

기본 HTML파일은 페이지 내부의 다른 객체를 그 객체의 URL로 참조한다.(예를 들어 html이 이미지를 참조할 때 localhost:3000/example.png로 참조하듯이), 각 html파일은 객체하나로 취급된다.

각 URL은 객체를 가지고 있는 서버의 호스트 네임과 객체의 경로 이름을 갖고있다.

웹 서버는 URL로 각각을 지정할 수 있는 웹 객체를 가지고있다. 가장 인기있는 웹 서버로는 아파치가 있다.

HTTP는 웹 클라이언트가 웹 서버에게 웹페이지를 어떻게 요청하는지와 서버가 클라이언트로 어떻게 웹 페이지를 전송하는지를 정의한다.

HTTP는 TCP를 전송 프로토콜로 사용한다.

HTTP 클라이언트는 먼저 서버에 TCP연결을 시작한다. 연결이 이루어지면 브라우저와 서버 프로세스는 그들의 소켓 인터페이스를 통해 TCP로 접속한다. 

HTTP에서 서버는 클라이언트에 관한 어떠한 상태정보도 기억하지 않는데, 같은 요청이 들어와도 같은 처리를 할 뿐 이전에 들어왔던 요청이라고 거부하거나 그러지 않는다. 이러한 특성 때문에 비상태 프로토콜(staless protocol)이라고 한다.

+ 각 요구 / 응답이 분리된 TCP연결을 통해 보내진다 - 비지속 연결(non-persistent connection)
  + 기본 모드에서 대부분의 브라우저는 5 ~ 10개의 동시 TCP연결을 허용하고 각 연결은 하나의 요청만을 처리한다.
  + 각 tcp연결을 설정해야하는 오버헤드가 각 요청마다 생긴다.(3-handshaking)
  + 각 요청 객체에 대한 새로운 연결이 설정이 설정되고 유지되어야한다.
    + TCP 버퍼가 할당되어야하고 TCP 변수들이 클라이언트와 서버 양쪽에서 유지되어야한다.
    + 수 많은 클라이언트를 다루는 서버에 심각한 부담을 줄 수 있다.

+ 각 요구 / 응답이 같은 TCP연결을 통해 보내진다 - 지속 연결(persistent connection)
  + http의 default 모드
  + 응답을 보낸 후에도 연결을 끊지않고 유지한다.
  + 각 요청들은 진행 중인 요청에 대한 응답을 기다리지 않고 연속해서 만들어질 수 있다.(파이프라이닝)
  + 일반적으로 HTTP서버는 일정 기간 사용되지 않으면 연결을 닫는다.



HTTP에는 메시지 포멧이 두 가지 있으며 이는 요청 메시지 포멧과 응답 메시지 포멧이다.

![스크린샷 2021-12-13 04 03 14](https://user-images.githubusercontent.com/48282185/145725847-a819c6bf-a746-4c97-8b0f-b5a377fbd519.png)

![image](https://user-images.githubusercontent.com/48282185/145725882-4c2d4a0f-a539-40d8-b704-d7366e70d2b0.png)

### 요청 메시지의 특징

+ 메시지가 ASCII 텍스트로 쓰여 있어 사람이 읽을 수 있다.
+ 메시지의 각 줄은 LF(line feed)와 CR(Carriage Return)로 구별된다.
+ 요청 메시지의 첫 번째라인은 3개의 필드로 구성된다.(요청 / URL / 버전) - POST(방식) /(URL) HTTP/1.1(HTTP 버전)
+ GET방식은 브라우저가 URL필드로 식별되는 객체를 요청할 때 사용한다. 
+ 이미 TCP연결이 맺어져있어 호스트를 이미 알고 있는데 왜  HOST를 필요로 하는가?  캐시를 위해
+ Connection: close는 서버가 요청 객체를 보내고 연결 닫기를 희망한다를 의미
+ User-agent는 서버에 요청하는 디바이스오 ㅏ브라우저 등 사용자 소프트웨어의 식별 정보를 담고있다. 아래의 상황에 주로 사용된다. [참고](https://d2.naver.com/helloworld/6532276)
  + 특정 버전의 버그
  + OS의 동작 차이
  + 버전에 따른 동작 차이
  + 사용자 에이전트에 따라 보여줄 콘텐츠 협상

### 응답 메시지의 특징

+ 시작 라인은 http 버전 / 상태 코드 / 상태 코드에 따른 메시지
+ server는 메시지가 아파치 웹서버에의해 만들어졌음을 나타냄, user-agent와 비슷한 역할
+ Content-type은 개체 몸체 내부의 객체의 데이터 형태를 지칭한다.
+ Date는 HTTP응답이 서버에 의해 생성되고 보낸 날짜와 시간을 나타낸다. 서버가 파일 시스템으로부터 객체를 추출하고 응답 메시지에 그 객체를 삽입하여 응답 메시지를 보낸 시간을 의미
+ Content-Length: Byte단위이고 송신되는 객체의 크기이다.
+ Last-Modifiend: 객체가 생성되거나 마지막으로 수정된 시간과 날짜를 나타냄 로컬 클라이언트와 네트워크 캐시서버에서의 객체 캐싱에 매우 중요한 역할을 한다. 

## 쿠키

서버가 사용자 접속을 제한하거나 사용자에 따라 콘텐츠를 제공하기를 원하므로 웹 사이트가 사용자를 확인하는 것이 바람직할 때가 있다. 이 목적으로 HTTP는 쿠키를 사용한다.

서버는 처음 접속한 유저를 대상으로 식별번호를 만들고 이 식별번호로 인덱스 되는 백엔드 데이터베이스 안에 엔트리를 만든다. 이후 서버는 응답하는데, 이 HTTP 응바에 식별번호를 담고있는 Set-cookie헤더가 포함된다. 브라우저는 관리하는 특정한 쿠키 파일에 서버의 호스트 네임과 Set-cookie헤더를 통해 전달받은 식별번호를 저장한다. 이후 브라우저에서 서버로 요청할 때 이 쿠키 파일에서 식별번호를 찾아 HTTP요청에 넣는다.

이 쿠키를 이용하여 사용자의 활동을 추적할 수 있다. 이후 사용자가 재접속해도 이전 활동을 저장하고 있기 때문에 계속 이어서 할 수 있도록 이전 페이지 복원이라던가 그런 것을 해줄 수 있다. 

쿠키는 비상태 HTTP 위에서 사용자 세션 계층을 생성하는데 이용되어 세션 시간동안 사용자를 식별하는 역할을 한다.



## 웹 캐시

웹 캐시(Proxy server)는 origin의 웹 서버를 대신하여 HTTP 요구를 충족시키느 네트워크 개체이다.

웹 캐시는 자체의 저장 매체를 가지고 있어 최근 호출된 객체의 사본을 저장 및 보존한다.

브라우저는 사용자의 모든 HTTP요구가 웹 캐시에 가장 먼저 보내지도록 구성될 수 있다.

캐시는 서버이면서 클라이언트라는 점을 유의한다. 왜냐하면 클라이언트의 요청에 응답할 수도 있고, origin 서버에 요청을 할 수도 있기 때문이다.

### 웹 캐시의 장점

+ 요구에 대한 응답 시간을 줄일 수 있다. 특히 origin 서버와 클라이언트 사이의 병목 대역폭이 클라이언트와 캐시 사이의 병목 대역폭에 비해 매우 작을 때 더욱 효과적이다. (클라이언트와 캐시 사이에 높은 속도의 연결이 설정되어있는 경우)
+ 한 기관에서 인터넷으로 접속하는 링크상의 웹 트래픽을 대폭으로 줄일 수 있다.(비용 절감과 직결)

### 웹 캐시의 종류

+ 브라우저 캐시 - 브라우저의 로컬 저장소와 캐시에 이전에 방문한 웹페이지의 정적 자원을 저장해 사용
  + [브라우저 캐시 - 토스](https://toss.tech/article/smart-web-service-cache)
  + [브라우저 캐시 - 블로그]( https://sarc.io/index.php/miscellaneous/1565-browser-cache)
+ 프록시 웹 캐시 - 웹 서버와 클라이언트 사이의 프록시 서버이다.
+ CDN - 웹 캐시는 많은 트래픽을 지역화 하고있다.
+ ISPs - 브라우저 캐시와 유사하게 동작하지만, 브라우저 캐시와 다르게 사용자가 임시 저장된 파일을 지울 수 없고, 캐시가 만료되기까지 기다려야한다.(일반적으로 웹 캐시는 ISP가 구입하고 설치한다. ISP는 하나 이상의 캐시를 네트워크상에 설치하고 설치된 캐시를 가리키도록 브라우저를 미리 설정한다.)

![image](https://user-images.githubusercontent.com/48282185/145728425-a0a67f04-7b59-4ece-98b1-f2cac637b4c6.png)

[참고](https://snoop-study.tistory.com/62)

### 조건부 GET

캐시가 제공하는 객체가 최신이 아닐 수 있다는 것이 캐시를 사용함에 있어서 가장 큰 문제이다. 이러한 문제를 해결하고자 HTTP는 모든 객체들이 최신의 것임을 확인하면서 캐싱하는 방식을 갖고 있다. 이러한 방식을 조건부 GET이라고 한다. HTTP 요청 메시지가 (1)GET방식을 사용하고, (2)If-Modified-Since헤더라인을 포함하고 있다면 이것이 조건부 GET메시지이다.

1. 브라우저를 대신해 캐시가 웹 서버에 요청을 보낸다. 

2. 웹 서버는 Last-Modified필드를 포함한 응답을 보내준다
3. 캐시는 요청하는 브라우저에게 객체를 보내주고 자신도 객체를 저장한다. 키포인트는 캐시가 객체와 더불어 마지막으로 수정된 날짜를 저장한다는 것이다.
4. 이 객체는 지난주에 웹 서버에서 수정되었으므로 브라우저는 조건부 GET으로 갱신 조사를 수행한다.
5. If-Modified-since필드에 적힌 날짜 이후 수정된 경우에만 그 객체를 보낸다. 만약 수정되지 않았다면 empty body가 리턴되고 이 때 상태코드는 304 Not Modified이다 이는 요청 객체의 캐시된 복사본을 사용하라는 것을 의미한다.

### 프록시의 종류

+ [리버스 프록시 vs 포워드 프록시](https://bcp0109.tistory.com/194)

## DNS

## CDN

## 스트리밍



+ http를 이용한 파일 전송 방식 궁금
+ formData, blob, stream요런거 잘 모르겠음..
+ 웹개발에서 쿠키 주로 언제쓰는가
# 8.Boundaries

### 외부 코드 사용하기

```java
  Map Sensors = new HashMap();

  Sensor s = (Sensor)sensors.get(sensorId);
```

Map이 반환하는 Object를 올바른 유형으로 변환할 책임은 Map을 사용하는 클라이언트에 있다.

```java
  Map<String, Sensor> sensors = new HashMap<Sensor>();
  ...
  Sensor s = sensors.get(sensorId);
```
위와 같이 제너릭스를 사용하여 코드 가독성을 높이곤 한다.
그렇지만 Map<String, Sensor> 가 사용자에게 필요하지 않은 기능까지 제공한다 는 문제는 해결 못함
Map 인터페이스가 변할경우 다 변경해야 한다.

Map을 좀 더 깔끔하게 사용한 코드

```java
  public class Sensors {
    private Map sensors = new HashMap();

    public Sensor getById(String id) {
      return (Sensor) sensors.get(id);
    }

    // 이하 생략
  }
```

Map을 Sensors 안으로 숨긴다. Map 인터페이스가 바뀌더라도 나머지 프로그램에는 영향이 없다.
Sensors 클래스 안에서 객체 유형을 관리하고 변환하기 때문

Map 클래스를 사용할 때마다 캡슐화 하라는 소리가 아니라 Map을 여기저기 넘기지 말라는 말.

### 경계 살피고 익히기
외부 코드를 가져올때도 테스트는 필요하고 이를 위해 필요한 테스트가 학습 테스트라고 한다

### log4j 익히기
안읽고 넘어감

### 학습 테스트는 공짜 이상이다.
학습 테스트는 패키지가 예상대로 도는지 검증한다.
새 버전을 도입했을때 검증하는 용도로 사용할 수 있다.

### 아직 존재하지 않는 코드를 사용하기
아는 코드와 모르는 코드를 분리하는 경계.


### 깨끗한 경계
경계에 위치하는 코드는 깔끔히 분리한다. 기대치를 정의하는 테스트 케이스도 작성한다.

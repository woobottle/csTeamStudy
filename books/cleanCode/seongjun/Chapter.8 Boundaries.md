# Boundaries

## Using Third-Party Code

* 제공자는 범용성 있게 짜려고 노력한다

* 사용자는 자신의 요구에 집중하는 인터페이스를 바란다.

* `java.util.Map` 은 다양한 인터페이스로 수많은 기능을 제공한다.

  * 여기저기 넘기면서 사용한다 가정하면 - 누군가 clear() 메서드를 사용해서 지울 가능성  / 권한이 충분히 있다.
  * 특정 유형만 저장하기로 결정했다면? 누가 추가해도 ..
  * `Map sensors = new HasnMap();`
  * `Sensor s = (Sensor)sensors.get(sensorId);`
    * object를 올바른 유형으로 변환할 책임은 map을 사용하는 클라이언트에 있다.
    * 코드 의도도 분명히 드러나지 않음

* Generics를 사용하면 가독성 높아짐

* `Map<String, Sensor> sensors = new HashMap<Sensor>();`

* `Sensor s = sensors.get(sensorId);`

  * `Map<String, Sensor>` 인스턴스를 여기저기 넘긴다면, Map이 변경되었을 때 수정할 코드가 상당히 많아진다.

* ```java
  public class Sensors {
    private Map sensors = new HashMap();
    public Sensor getById(String id) { 
      return (Sensor)sensors.get(id);
  	}
  ..
  }
  ```

* Map을 숨긴다. 따라서 map 인터페이스가 변해도, 나머지 프로그램에는 영향 X

* Seonsor클래스 안에서 객체 유형을 관리하므로 제너릭 쓰든 아니든 문제 X

* 매번 캡슐화하라는게 아닌 여기저기 넘기지 말라는거다



## Exploring and Learning Boundaries

* 우리 버그인지 라이브러리 버그인지 디버깅하느라 골치
* 외부 코드 익히고 통합하는건 어렵다.
* 학습테스트
  * 우리 쪽 코드를 작성해 외부 코드를 호출하는 대신 먼저 간단한 테케를 작성해 외부 코드를 익힌다?
  * 프로그램에서 사용하려는 방식대로 외부 API를 호출한다
  * 통제된 환경에서 API를 제대로 이해하는지를 확인하는 셈



### Learning log4j

...

## Learning Tests Are Better Than Free

* 드는 비용이 없다. 어쨋든 API 배워야하니까.. 오히려 필요한거만 확보
* 새버전 나오면 테스트 돌려서 차이 확인 - 새버전 적용이 쉽다.

### Using Code That Does Not Yet Exist

* 아직 구현이 안된 / 혹은 모르는 코드를 우리가 바라는 인터페이스로 구현한다?
* Adapter 패턴으로 api 사용을캡슐화해 api가 바뀔때 수정할 코드를 한곳으로 모음
* Fake 클래스를 하나 사용해서 테스트한다.

### Clean Boundaries

* 설계가 우수한, 깨끗한 경계를 갖고있으면 변경에 많은 투자와 재작업이 필요 X
* 깔끔하게 분리한다. 
* 기대치를 정의하는 테케도 작성한다.
* 통제 불가능의 외부 패키지에 의존하는 대신, 통제가 가능한 우리 코드에 의존하자.
* 외부 패키지를 호출하는 코드를 줄여 경계를 관리하자.
* 새로운 클래스로 래핑하거나 adapter 패턴을 사용해 원하는 인터페이스를 패키지가 제공하는 인터페이스로 변환하자.
* 




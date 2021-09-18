# 1. UnitTest

### TDD 법칙 세 가지

1. 실패하는 단위 테스트를 작성할 때까지 실제 코드를 작성하지 않는다.
2. 컴파일은 실패하지 않으면서 실행이 실패하는 정도로만 단위 테스트를 작성한다.
3. 현재 실패하는 테스트를 통과할 정도로만 실제 코드를 작성한다.

### 깨끗한 테스트 코드 유지하기

테스트 코드는 실제 코드 못지 않게 중요하다. => 아직 접해보질 못했다.

* 테스트는 유연성, 유지보성, 재사용성을 제공한다
코드에 유연성, 유지보수성, 재사용성을 제공하는 버팀목이 바로 단위 테스트다.
테스트 케이스 들이 잠정적인 버그를 잡아줄 수 있으니까 그만큼 중요하게 강조하는 것 같다.

### 깨끗한 테스트 코드
가독성은 실제 코드보다 테스트 코드에 더더욱 중요하다.

```java
  public void testGetPageHierachyAsXml() throws Exception {
    makePages("PageOne", "PageOne.ChildOne", "PageTwo");

    submitRequeset("root", "type:pages");

    assertResponseIsXML();
    assertResponseContains(
      "<name>PageOne</name>", "<name>PageTwo</name>", "<name>ChildOne</name>"
    );
    assertResponseDoesNotContain("SymPage");
  }

  public void testGetDataAsXml() throws Exception {
    makePageWithContent("TestPageOne", "test page");

    submitRequest("TestPageOne", "type:data");

    assertResponseIsXML();
    assertResponseContains("test page", "<Test");
  }
```
* 도메인에 특화된 테스트 언어
* 이중 표준

```java
  @Test
  public void turnOnLoTempAlarmAtThreshold() throws Exception {
    hw.setTemp(WAY_TOO_COLD);
    controller.tic();
    assertTrue(hw.heaterState());
    assertTrue(hw.blowerState());
    assertTrue(hw.coolerState());
    assertTrue(hw.hiTempAlarm());
    assertTrue(hw.loTempAlarm());
  }

  @Test
  public void turnOnLoTempAlarmAtThreshold() throws Exception {
    wayTooCold(); // tic 함수는 이안에 숨어있다
    assertEquals("HBchL", hw.getState()); // 대문자는 켜졌는지 소문자는 꺼졌는지
  }

  @Test
  public void turnOnCoolerAndBlowerIfTooHot() throws Exception {
    tooHot();
    assertEquals("hBChl", hw.getState());
  }
```
### 테스트 당 assert 하나

assert는 boolean이 false일 경우 AssertionError 발생시키는 명령어

### 테스트 당 개념 하나
테스트 함수마다 한 개념만 테스트 하라

```java

  // 3개의 테스트 케이스 모두 분리해서 관리하여야 한다.
  public void testAddMonths() {
    SerialDate d1 = SerialDate.createInstance(31, 5, 2004);

    // 다음달 30일인 경우
    SerialDate d2 = SerialDate.addMonths(1, d1);
    assertEquals(30, d2.getDayOfMonth());
    assertEquals(6, d2.getMonth());
    assertEquals(2004, d2.getYYYY());

    // 다다음달 31일인 경우
    SerialDate d3 = SerialDate.addMonths(2, d1);
    assertEquals(31, d2.getDayOfMonth());
    assertEquals(7, d2.getMonth());
    assertEquals(2004, d2.getYYYY());
    
    // 한달 더한거의 addMonth는 30일인 경우
    SerialDate d3 = SerialDate.addMonths(1, SerialDate.addMonths(1, d1));
    assertEquals(30, d2.getDayOfMonth());
    assertEquals(7, d2.getMonth());
    assertEquals(2004, d2.getYYYY());
  }
```

### FIRST

* 빠르게(Fast) => 테스트는 빨라야 한다. 빨리 돌아야 한다.
* 독립적으로(Indpendent) => 각 테스트는 서로 의존하면 안 된다.
* 반복가능하게(Repeatable) => 어떤 환경에서도 반복 가능해야 한다. 어떤 환경이라도 반복적으로 돌아갈수 있어야 한다.(네트워크가 연결이 되어있지 않더라도)
* 자가검증하는(Self-Validating) => boolean 값으로 결과를 내야 한다.
* 적시에(Timely) => 테스트는 적시에 작성해야 한다. 실제 코드를 구현하기 직전에 구현한다.
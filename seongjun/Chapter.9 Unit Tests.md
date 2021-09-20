# Unit tests

* TDD가 하테하테

## The Three Laws of TDD

1. 실패하는 단위테스트를 작성할 때까지 실제코드를 작성하지 않는다.
2. 컴파일은 실패하지 않으면서 실행이 실패하는 정도로만 단위 테스트를 작성한다.
3. 현재 실패하는 테스트를 통과할 정도로만 실제 코드를 작성한다.

* 개발과 테스트가 30초 주기로 묶인다. 테스트 코드가 실제 코드보다 몇 초 전에 나온다.
* 매일 수십 개,... 뭐 많은 테케가 나오는데 심각한 관리문제 유발

## Keeping Tests Clean

* 테스트 코드는 실제 코드 못지 않게 중요하다. 잘짜야함

### Tests Enable the -ilities / 유연성 유지보수성 재사용성

* 유연성, 유지보수성, 재사용성을 제공하는 버팀목이 바로 단위테스트이다.
* 테스트 케이스가 없으면 모든 변경이 잠정적인 버그다.
* 변경을 주저하게됨 커버리지가 높으면 공포가 줄어든다. 오히려 안심하고 아키텍쳐와 설계를 개선한다. - 변경이 쉬워진다.

### Clean Tests

* 가독성 * 9999

```java
public void testGetPageHieratchyAsXml() 
  throws Exception {
		crawler.addPage(root, .parse("PageOne")); 		
  	crawler.addPage(root, PathParser.parse("PageOne.ChildOne")); 
  	crawler.addPage(root, PathParser.parse("PageTwo"));
  
		request.setResource("root"); 
  	request.addInput("type", "pages");
		Responder responder = new SerializedPageResponder(); 
  	SimpleResponse response =
			(SimpleResponse) responder.makeResponse( 
      new FitNesseContext(root), request);
		String xml = response.getContent();
  
		assertEquals("text/xml", response.getContentType()); 
  	assertSubString("<name>PageOne</name>", xml); 
  	assertSubString("<name>PageTwo</name>", xml); 
  	assertSubString("<name>ChildOne</name>", xml);
}

public void testGetPageHieratchyAsXmlDoesntContainSymbolicLinks() throws Exception
{
	WikiPage pageOne = crawler.addPage(root, PathParser.parse("PageOne")); 
  crawler.addPage(root, PathParser.parse("PageOne.ChildOne")); 
  crawler.addPage(root, PathParser.parse("PageTwo"));
  
	PageData data = pageOne.getData();
	WikiPageProperties properties = data.getProperties();
	WikiPageProperty symLinks = properties.set(SymbolicPage.PROPERTY_NAME);
  symLinks.set("SymPage", "PageTwo");
	pageOne.commit(data);
  
	request.setResource("root"); 
  request.addInput("type", "pages");
	Responder responder = new SerializedPageResponder(); 
  SimpleResponse response =
		(SimpleResponse) responder.makeResponse( 
    	new FitNesseContext(root), request);
	String xml = response.getContent();
  
	assertEquals("text/xml", response.getContentType()); 
  assertSubString("<name>PageOne</name>", xml); 
  assertSubString("<name>PageTwo</name>", xml); 
  assertSubString("<name>ChildOne</name>", xml); 
  assertNotSubString("SymPage", xml);
}

public void testGetDataAsHtml() throws Exception {
	crawler.addPage(root, PathParser.parse("TestPageOne"), "test page");
	request.setResource("TestPageOne"); 
  request.addInput("type", "data");
  
	Responder responder = new SerializedPageResponder(); 
  SimpleResponse response =
		(SimpleResponse) responder.makeResponse( 
	    new FitNesseContext(root), request);
	String xml = response.getContent();
  
	assertEquals("text/xml", response.getContentType()); 
  assertSubString("test page", xml); 
  assertSubString("<Test", xml);
}
```

* `PathParser` 는 문자열을 `pagePath` 인스턴스로 변환한다.
* `pagePath`는 크롤러가 사용하는 객체다.
* 이 코드는 테스트와 무관하고, 테스트 코드의 의도만 흐린다.
* responder 객체를 생성하는 코드와 response를 수집해 변환하는 코드 역시,
* resource와 인수에서 요청 url을 만드는 어설픈 코드

```java
public void testGetPageHierarchyAsXml() throws Exception { 
  makePages("PageOne", "PageOne.ChildOne", "PageTwo");
	submitRequest("root", "type:pages");
	assertResponseIsXML(); 
  assertResponseContains(
		"<name>PageOne</name>", "<name>PageTwo</name>", "<name>ChildOne</name>" );
}
public void testSymbolicLinksAreNotInXmlPageHierarchy() throws Exception { 
  WikiPage page = makePage("PageOne");
	makePages("PageOne.ChildOne", "PageTwo");
	addLinkTo(page, "PageTwo", "SymPage"); 
  submitRequest("root", "type:pages");
	assertResponseIsXML(); 
  assertResponseContains(
"<name>PageOne</name>", "<name>PageTwo</name>", "<name>ChildOne</name>" );
	assertResponseDoesNotContain("SymPage"); 
}
  
public void testGetDataAsXml() throws Exception { 
  makePageWithContent("TestPageOne", "test page");
	submitRequest("TestPageOne", "type:data");
	assertResponseIsXML();
	assertResponseContains("test page", "<Test"); 
}
```

* BUILD - OPERATE - CHECK 패턴
* 테스트 자료를 만든다 - 테스트 자료를 조작한다 - 결과가 올바른지 확인한다.

### Domain Specific Testing Language

* DSL로 테스트 코드를 구현하는 기법
* 흔히 쓰는 api를 사용하는 대신 위에 함수와 유틸리티를 구현하고, 그걸 써서 코드를 읽기 쉽게
* 테스트코드에서 사용하는 특수 api 가 된다.
* 첨부터 설계된게 아닌 리펙토링

### A Dual Standard

* 실제 코드에 적용하는 표준과 확실히 다르다.

```java
@Test
public void turnOnLoTempAlarmAtThreashold() throws Exception {
	hw.setTemp(WAY_TOO_COLD); 
  controller.tic(); 
  assertTrue(hw.heaterState()); 
  assertTrue(hw.blowerState()); 
  assertFalse(hw.coolerState()); 
  assertFalse(hw.hiTempAlarm()); 
  assertTrue(hw.loTempAlarm());
}
```

```java
@Test
public void turnOnLoTempAlarmAtThreshold() throws Exception {
	wayTooCold();
	assertEquals("HBchL", hw.getState()); 
}
```

* 대문자는 켜짐, 소문자는 꺼짐? - 항상 HBCHL 순서다... .?
* 

```java
@Test
public void turnOnCoolerAndBlowerIfTooHot() throws Exception {
	tooHot();
	assertEquals("hBChl", hw.getState()); 
}
@Test
public void turnOnHeaterAndBlowerIfTooCold() throws Exception {
	tooCold();
	assertEquals("HBchl", hw.getState()); 
}
@Test
public void turnOnHiTempAlarmAtThreshold() throws Exception {
	wayTooHot();
	assertEquals("hBCHl", hw.getState()); 
}
@Test
public void turnOnLoTempAlarmAtThreshold() throws Exception {
	wayTooCold();
	assertEquals("HBchL", hw.getState()); 
}
```

* 흉하다 

```java
public String getState() {
	String state = "";
	state += heater ? "H" : "h"; 
  state += blower ? "B" : "b"; 
  state += cooler ? "C" : "c"; 
  state += hiTempAlarm ? "H" : "h"; 
  state += loTempAlarm ? "L" : "l"; 
  return state;
}
```

### One Assert per Test 

* 가혹한 규칙이지만 장점이 있음

* ```java
  public void testGetPageHierarchyAsXml() throws Exception { 
    givenPages("PageOne", "PageOne.ChildOne", "PageTwo");
  	whenRequestIsIssued("root", "type:pages");
  	thenResponseShouldBeXML(); 
  }
  public void testGetPageHierarchyHasRightTags() throws Exception { 
    givenPages("PageOne", "PageOne.ChildOne", "PageTwo");
  	whenRequestIsIssued("root", "type:pages");
  	thenResponseShouldContain(
  		"<name>PageOne</name>", "<name>PageTwo</name>", "<name>ChildOne</name>"
  	); 
  }
  ```

* 9-2처럼 Xml이다 / 특정 문자열을 포함한다 - 를 병합하는건 어렵다.. 따라서 나눔

* given-when-then  관례를 사용

* 테스트를 분리하니 중복이 늘어났다.
  * TEMPLATE METHOD 패턴을 사용하여 중복을 제거한다.
  * given/when 부분을 부모 클래스에 두고 then 부분을 자식클래스에 둔다.
  * 독자적인 테스트 클래스를 만들어 @Before 에 , @Test에 ..
* 뭐 무튼 배보다 배꼽이 더 크다.
* 그냥 여러 assert 문을 넣는다 - 단지 줄여야한다고 생각할뿐

### Single Concept per Test

* 테스트 함수마다 한 개념만 테스트
* 독자적인 개념 세 개를 테스트하므로 , 세 개로 쪼개야함

```java
public void testAddMonths() {
	SerialDate d1 = SerialDate.createInstance(31, 5, 2004);
	SerialDate d2 = SerialDate.addMonths(1, d1);
  assertEquals(30, d2.getDayOfMonth()); 
  assertEquals(6, d2.getMonth()); 
  assertEquals(2004, d2.getYYYY());
  
	SerialDate d3 = SerialDate.addMonths(2, d1); 
	assertEquals(31, d3.getDayOfMonth()); 
	assertEquals(7, d3.getMonth()); 
	assertEquals(2004, d3.getYYYY());
	
	SerialDate d4 = SerialDate.addMonths(1, SerialDate.addMonths(1, d1)); 
	assertEquals(30, d4.getDayOfMonth());
	assertEquals(7, d4.getMonth());
	assertEquals(2004, d4.getYYYY());
}
```

* 31일로 끝나는 달의 마지막 날짜가 주어지는 경우
  * 30일로 끙ㅌ나는 한달을 더하면 날짜가 30일이 되어야지 31일이 되면 안됨
  * 두 달을 더하면 그리고 두 번째 달이 31일로 끝나면 날짜는 31일 되어야한다

* 30일로  끝나는 달의 마지막 날짜가 주어지는 경우
  * 31일로 뭐시기 어ㅓ구



## F I R S T

### Fast 

* 빨리돌아야함
* 느리면 자주 돌릴 엄두를 못낸다. 그럼 정리도 쉽지않고...

### Independent

* 각 테스트는 서로 의존하면 안된다. 한 테스트가 다음 테스트가 실행될 환경을 준비 X
* 어떤 순서로 실행해도 괜찮아야함

### Repeatable

* 테스트는 어떤 환경에서도 반복 가능해야한다.
* 실제환경, QA환경, 네트워크가 연결되지 않은 환경에서도 .

### Self-Validating

* bool값으로 결과를 내야한다. 성공 아니면 실패임

### Timely

* 적시에 작성되어야한다.
* 실제 코드를 구현하기 직전에 구현한다. 실제 코드를 구현한 다음 테스트 코드를 만들면 실제 코드가 어렵다고 ...



## 결론

* 테스트 코드는 실제 코드만큼이나 중요하고, 유연성, 유지보수성, 재사용성을 보존하고 강화한다.
* 테스트 API를 구현해 DSL을 만들자. 그러면 쉬워진다.






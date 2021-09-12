# 3. Functions

```java
// 3-1
public static String testableHtml(
  PageData pageData,
	boolean includeSuiteSetup
) throws Exception {
	WikiPage wikiPage = pageData.getWikiPage(); 
  StringBuffer buffer = new StringBuffer(); 
  if (pageData.hasAttribute("Test")) {
		if (includeSuiteSetup) { 
      WikiPage suiteSetup =	PageCrawlerImpl.getInheritedPage( SuiteResponder.SUITE_SETUP_NAME, 				wikiPage);
			if (suiteSetup != null) {
				WikiPagePath pagePath = suiteSetup.getPageCrawler().getFullPath(suiteSetup);
				String pagePathName = PathParser.render(pagePath);
				buffer.append("!include -setup .").append(pagePathName) .append("\n");
			}
    }
		WikiPage setup = PageCrawlerImpl.getInheritedPage("SetUp", wikiPage);
		if (setup != null) { 
      WikiPagePath setupPath =wikiPage.getPageCrawler().getFullPath(setup);
			String setupPathName = PathParser.render(setupPath);
      buffer.append("!include -setup .").append(setupPathName) .append("\n");
		}
  }
	buffer.append(pageData.getContent());
	if (pageData.hasAttribute("Test")) {
		WikiPage teardown = PageCrawlerImpl.getInheritedPage("TearDown", wikiPage);
		if (teardown != null) { 
      WikiPagePath tearDownPath = wikiPage.getPageCrawler().getFullPath(teardown);
			String tearDownPathName = PathParser.render(tearDownPath);
      buffer.append("\n").append("!include -teardown .") .append(tearDownPathName) .append("\n");
		}
  if (includeSuiteSetup) {
		WikiPage suiteTeardown = PageCrawlerImpl.getInheritedPage( SuiteResponder.SUITE_TEARDOWN_NAME, wikiPage);
		if (suiteTeardown != null) {
			WikiPagePath pagePath = suiteTeardown.getPageCrawler().getFullPath (suiteTeardown);
			String pagePathName = PathParser.render(pagePath); 
      buffer.append("!include -teardown .").append(pagePathName) .append("\n");
		} 
  }
} pageData.setContent(buffer.toString());
 return pageData.getHtml();
}

```

* 추상화 수준이 다양하다
* 코드가 길다
* 중첩 if문은 이상한 플래그를 확인하고 이상한 문자열을 사용하고, 이상항 함수를 호출한다

```java
// 3-2
public static String renderPageWithSetupsAndTeardowns( 
  PageData pageData, boolean isSuite
) throws Exception {
	boolean isTestPage = pageData.hasAttribute("Test"); 
  if (isTestPage) {
    WikiPage testPage = pageData.getWikiPage(); 
    StringBuffer newPageContent = new StringBuffer(); 
    includeSetupPages(testPage, newPageContent, isSuite); 
    newPageContent.append(pageData.getContent()); 
    includeTeardownPages(testPage, newPageContent, isSuite); 
    pageData.setContent(newPageContent.toString());
	}
	return pageData.getHtml(); 
}
```

* 100프로 이해하기엔 어렵지만, 함수가 setup page와 teardown페이지를 테스트 페이지에 넣은 후 랜더링한다는것은 짐작



## Small

```java
// 3-3
public static String renderPageWithSetupsAndTeardowns( 
  PageData pageData, boolean isSuite
) throws Exception { 
  if (isTestPage(pageData)) includeSetupAndTeardownPages(pageData, isSuite); 
  return pageData.getHtml();
}
```

* 조건문 / 반복문에 들어가는 블록은 한 줄이어야 한다. - 대개 거기서 함수를 호출
* 중첩 구조가 생길만큼 함수가 커져서는 안된다. 
* 들여쓰기가 1단/ 2단을 넘어서면 안된다.

## Do one Thing

*  `3-1` 은 여러 가지를 처리한다.
  * 버퍼를 생성, 페이지를 가져오고, 상속된 페이지를 검색하고, 경로를 렌더링 , 문자열 덧붙이고, html 생성

* `3-3`은 한 가지만 처리한다. 설정 페이지와 해제 페이지를 테스트 페이지에 넣는다.

##### 함수는 한 가지를 해야 한다. 그 한 가지를 잘 해야 한다. 그 한 가지만을 해야한다.

* `3-3` 이 한가지가 맞나? 세가지 아닌가?
  1. 페이지가 테스트 페이지인지 판단
  2. 맞다면 설정 페이지와 해제 페이지를 넣는다
  3. 페이지를 랜더링한다.

* 이 세 단계는  지정된 함수 이름 아래에서 추상화 수준이 하나이다. 

  * TO 문단 하나로 기술하자면 - like ruby,python def

    ```
    TO RednerPageWithSetupsAndTeardowns, we check to see whether the page is a test page and if so, we include the setups and teardowns. In either case we render the page in HTML
    ```

  * 3-2는 추상화 수준이 둘 / 3-3에서 더이상 축소 ㄴ 

  * if문을 함수로 추출해도 어차피 똑같은 내용을 다르게 표현할 뿐 추상화 수준은 바뀌지 않는다.

### Secions within functions

한가지만 하는 작업하는 함수는 자연스럽게 섹션으로 나누기 어렵다.

## One Level of Abstraction per Function

* `getHtml()` - 높은 추상화 수준
* `String pagePathName = PathParser.render(pagepath);` - 중간
* `.append('\n')`- 낮음
* 한 함수 내에 추상화 수준을 섞으면 코드를 읽는 사람이 헷갈린다.
* 특정 표현이 근본 개념인지, 세부 사항인지 구분하기 어렵다
* 근본 개념과 세부사항이 뒤섞이면 점점 세부사항이 추가됨

## Reading Code from Top to Bottom: The Stepdown Rule

* 코드는 위에서 아래로 읽혀야 좋다.

* 한 함수 다음에는 추상화 수준이 한 단계 낮은 함수가 온다. - 한 단계씩 낮아진다.

* TO 문단을 읽듯이 읽혀야한다

  ```
  TO include the setups and teardowns, we include setups then we include the test page content and then we include the teardowns
  
  	TO include the setups, we include the suite setup if this is a suite, then we include the regular setup.
  	
  	TO include the suite setup, we search the parent hierarchy for the "SuiteSetUp" page and add an include statement with the path of that page
  	
  	To search the parent ... 
  ```

* 하지만 추상화 수준이 하나인 함수를 구현하기란 쉽지 않다.

* see 3-7

## Switch Statement

* switch문은 작게 만들기 어렵다. '한 가지' 작업만 하는 switch 문도 만들기 어렵다. 본질적으로 N가지를 처리한다.
* 완전히 피할 순 없으니, 저차원 클래스에 숨기고 절대로 반복하지 않는 방법을 쓴다
  * 다형성 사용

```java
public Money calculatePay(Employee e) 
  throws InvalidEmployeeType {
  switch (e.type) { 
    case COMMISSIONED:
		  return calculateCommissionedPay(e); 
    case HOURLY:
  		return calculateHourlyPay(e); 
    case SALARIED:
		  return calculateSalariedPay(e); 
    default:
		  throw new InvalidEmployeeType(e.type); 
  }
}
```

* 함수가 길다 - 새 직원 유형을 추가하면 더 길어진다.

* 한 가지 작업만 수행하지 않는다.

* SRP ( Single Responsibility Principle ) 를 위반한다. ( 단일 책임 )

* OCP ( Open Closed Principle )를 위반 ( 기존 코드를 고치지 않고 추가 가능 )

* 가장 심각한 문제는, 위와 동일한 구조의 함수가 무한정 존재한다.

  * `isPayday(Employee e, Date date);`
  * `deliverPay(Employee e, Money pay);`

  

```java
//3-5	
public abstract class Employee {
	public abstract boolean isPayday();
  public abstract Money calculatePay();
  public abstract	void deliverPay(Money pay);
}
//-----------------
public interface EmployeeFactory {
public Employee makeEmployee(EmployeeRecord r) 
  throws InvalidEmployeeType; 
}
//-----------------
public class EmployeeFactoryImpl implements EmployeeFactory {
	public Employee makeEmployee(EmployeeRecord r) 
    throws InvalidEmployeeType { 
    switch (r.type) {
			case COMMISSIONED:
				return new CommissionedEmployee(r) ;
			case HOURLY:
				return new HourlyEmployee(r);
			case SALARIED:
				return new SalariedEmploye(r);
			default:
				throw new InvalidEmployeeType(r.type);
		}
  }
}
```



* 추상 팩토리에 숨기고, 보여주지 않는다.
* switch문으로 적절한 Employee 파생 클래스의 인스턴스를 생성
* calculatePay, isPayday, deliverPay 등의 함수는 Employee 인터페이스를 거쳐 호출된다, 다형성으로 실제 파생 클래스의 함수가 실행된다.
* 다형적 객체를 생성하는 코드 안에서만 switch를 참아주지!
  * 상속 관계롤 숨긴 후에는 절대로 다른 코드에 노출하지 않는다.
  * [G23] 물론 불가피한 상황도 생김



## Use descriptive Names

* `3-7` 에서 `testableHtml` => `SetupTeardownIncluder.render` 로 변경함
* isTestable, includesetupAndTeardownPages 등의 서술적인 이름을 썻음
* 여러 단어가 쉽게 읽히는 명명법을 사용한다.
* 여러 단어를 사용해 함수의 기능을 잘 표현하는 이름을 선택한다.
* 일관성이 있어야한다. 함수는 같은 문구, 명사, 동사를 사용한다.



## Function Arguments

* 제일 이상적인 인수는 무항
* 그 다음은 1개 - 단항, 2항 (이항), 3개 이상은 피하는게 좋다.
* `includeSetupPageInto(new PageContent)` 보단 `includeSetupPage()` 가 이해하기 더 쉽다.
  * 둘이 추상화 수준이 다르다.
* 테스트 관점에서도 인수가 없는게 더 편함 당근
* 최선은 0, 차선은 1

### Common Monadic Forms - 단항 형식

* 인수에 질문을 던지는 경우

* 인수를 뭔가로 변환해 결관를 반환하는 경우

  * 56 명령과 조회를 분리하라?

* 이벤트 함수 - 입력 인수만 있다. 출력은 없음,

* 이를 제외하고 단항 함수는 피한다.

  * ex) `void includeSetupPageInto(StringBuffer pageText)` 

    * 변환 함수에서 출력 인수를 사용하면 혼란을 일으킨다.
      * 바꿔주는걸 하지 말라는건가?
    * 입력 인수를 변환하는 함수면 변환 결과는 반환값으로

  * ```
    Try to avoid any monadic functions that don’t follow these forms, for example, void includeSetupPageInto(StringBuffer pageText). Using an output argument instead of a return value for a transformation is confusing. If a function is going to transform its input argument, the transformation should appear as the return value. Indeed, StringBuffer transform(StringBuffer in) is better than void transform-(StringBuffer out), even if the implementation in the first case simply returns the input argument. At least it still follows the form of a transformation.
    ```

### Flag Arguments

* 플래그 극혐, 애초에 한번에 여러 가지를 처리한다고 대놓고 공표하는 셈이다.
* 3-7은 별 도리가 없음, 이미 위에서 플래그를 넘기고 예제함수 아래로만 구조를 조정했음
* 그래도 render(true)는 rednerForSuite() / renderForSingleTest()로 나눠야 마땅

### Dyadic Functions - 이항함수

* 인수 2개는 1보다 훨 어렵다. 
* 적절한 경우는 좌표계 점 정도? `new Point(0,0)`
* `writeField(name) ` / `writeField(outputStream, name)`
* `writeField` 를 outputStream 클래스 구성원으로 만들어 outputStream.writeField(name) 으로 호출하거나
* outputStream을 현재 클래스 member variable로 만들어 인수를 안넘기거나
* FieldWriter라는 클래스를 만들어 constructor에서 outputStream을 받고 write 메서드를 구현한다.

### Triads - 삼항함수

* 

### Argument Objects

* 인수가 2-3개 필요하면 일부를 독자적인 클래스 변수로 선언할 가능성을 생각해본다.

* `Circle makeCircle(double x, double y, double radius)`

  `Circle makeCircle(Point center, double radius)`

  * 눈 속임처럼 보인다 할 수 있지만 x,y를 묶어서 넘기면서 개념을 표현하게된다.

### Argument Lists

* 때로 인수 개수가 가변적인 함수도 필요하다.
* `String.format("%s worked %.2f", name, hours)`
  * 가변 인수 부분을 list로 취급하면 , 사실상 이항함수 아님?
* 다 같은 원리가 적용된다, 하지만 이를 넘어서는 인수를 쓰면 문제가 있다.

## Verbs and Keywords

* write(name) - writeField(name) 
* assertEquals - assertExpectedEqualsActual(expected, actural)



## Have No Side Effects

* 사이드이펙트는 사기치는거임
* 함수에서 한가지를 하겠다고 약속해놓고, 남몰래 다른짓을 하는 것
* 클래스변수를 수정한다던지, 전역변수나 인수를 수정한다던지, 많은경우 temporal coupling이나 order dependency를 초래한다.

```java
//3-6
public class UserValidator {
	private Cryptographer cryptographer;
	public boolean checkPassword(String userName, String password) { 
    User user = UserGateway.findByName(userName);
		if (user != User.NULL) {
			String codedPhrase = user.getPhraseEncodedByPassword(); 
      String phrase = cryptographer.decrypt(codedPhrase, password); 
      if ("Valid Password".equals(phrase)) {
				Session.initialize();
				return true; 
      }
		}
	return false; 
  }
}
```

* 인수가 올바르면 true , 아니면 false 반환함
* 하지만 틀리면 session도 초기화 함 - 이름만 보고 호출하는 사용자는 인증하면서 기존 세션 지워버릴수도 있음
* 시간적인 결합을 초래한다 / 특정 상황에서만 호출이 가능하다는 뜻이다. 
  * 즉 세션 초기화해도 괜찮은 경우에만 호출이 가능함. 잘못 호출하면 세션정보가 날아감
  * 시간적인 결합이 필요하면 이름에 명시해라, - `checkPasswordAndInitializeSession`
  * 물론 한가지만 한다는 규칙을 위반한다.

## Output Arguments

* 인수를 함수 입력으로 해석한다.
* `appendFooter(s) ;` s에 푸터를 추가하는걸까? s라는 푸터를 추가하는걸까?
* `public void appendFooter(StringBuffer report)`
* 함수 선언부를 봐야 알 수 있음 - 애초에 보러 가는거 자체가 거슬린다 피하자
* 객체지향 전에는 불가피한 경우가 있었지만, 이제 거의 필요 없음 - 출력 인수로 쓰라고 설계한 변수가 this임
* `report.appendFooter()` 로 하자.
* 출력 인수는 피하고, 함수에서 상태를 변경해야 한다면 함수가 속한 객체 상태를 변경하는 식으로 



## Command Query Separation

* 함수는 뭔가를 수행하거나 답하거나 둘중 하나만 해야함. 둘다 하면 안된다

* 객체의 상태를 변경하거나, 정보를 반환하거나 둘중 하나다.

* `public boolean set(String attribute, String value);`

  * attr인 속성을 찾아 값을 value로 설정 한 후 성공하면 true, 아니면 false

  * `if(set("username", "unclebob"))...`

    * 확인하는건가? 설정하는건가? 동사지만 if문에 있으면 형용사같다. 
    * username을 unclebob으로 셋 해라 - username이 unclebob으로 셋 되어 있으면.? 

  * setAndCheckIfExsits로 바꿔도 되지만, 그냥 조회랑 분리

  * ```java
    
    if (attributeExists("username")) { 
    	setAttribute("username", "unclebob"); 
      ...
    }
    
    ```

## Prefer Exceptions to returning Error Codes - 오류 코드보다 예외

* 명령 함수에서 오류 코드를 반환하는 방식은 Command Query Separation 규칙을 미묘하게 위반한다.

* 자칫 if문에서 명령을 표현식으로 사용하기 쉬움

* `if (deletePage(page) == E_OK)`

  * 동사 형용사 혼란을 일으키지 않고, 여러 단계로 중첩되는 코드를 야기한다

  * 곧바로 오류코드를 처리해야함

  * ```java
    if (deletePage(page) == E_OK) {
    	if (registry.deleteReference(page.name) == E_OK) {
    		if (configKeys.deleteKey(page.name.makeKey()) == E_OK){ 
          logger.log("page deleted");
    		} else {
    			logger.log("configKey not deleted");
    		}
    	} else {
    		logger.log("deleteReference from registry failed"); 
      }
    } else {
    	logger.log("delete failed"); return E_ERROR;
    }
    ```

* 예외처리로 하면 분리되어서 깔끔함

* ```java
  
  try {
  	deletePage(page); 
  	registry.deleteReference(page.name); 
  	configKeys.deleteKey(page.name.makeKey());
  }
  catch (Exception e) {
  	logger.log(e.getMessage()); 
  }
  
  ```

## Extract Try/Catch Blocks

* 원래가 더러움 , 코드 구조에 혼란을 일으키고, 정상 동작과 오류처리 동작을 뒤섞는다ㅣ.

* 별도 함수로 뽑아내는게 좋다.

  ```java
  public void delete(Page page) { 
    try {
  		deletePageAndAllReferences(page); 
    }
  	catch (Exception e) { 
      logError(e);
  	} 
  }
  private void deletePageAndAllReferences(Page page) throws Exception { 
    deletePage(page);
  	registry.deleteReference(page.name); 
    configKeys.deleteKey(page.name.makeKey());
  }
  private void logError(Exception e) { 
    logger.log(e.getMessage());
  }
  ```

  * delete에서 모든 오류를 처리한다.
  * 실제 페이지를 제거하는 함수는 deletePageAndAllReferences 여기선 예외처리하지 않는다.

  

## Error Handling is One Thing

* 함수는 한 가지 작업만 해야하고 오류 처리도 한 가지에 속한다.



## The Error.java Dependency Magnet

* 오류 코드를 반환한다는 이야기는 클래스든 이넘이든 어딘가 오류 코드를 정의한다는 뜻이다.

* ```java
  public enum Error { 
    OK,
  	INVALID,
  	NO_SUCH,
  	LOCKED, OUT_OF_RESOURCES, WAITING_FOR_EVENT;
  }
  ```

* 위와 같은 클래스는 의존성 자석 - magnet 이다, 

* 다른 클래스에서 무조건 import 해 써야하므로 저게 변하면 다 재컴파일, 재배치 해야함 

* 예외를 사용하면 Exception 클래스에서 파생되므로 재배치 재컴파일 없이 새 예외 클래스를 추가할 수 있다. - OCP ( Open Closed Principle )



## Don't Repeat Yourself - DRY

* `3-1` 에서 Setup / Suite / Setup / TearDown / SuiteTearDown 에서 반복된다.

  * 다른 코드와 섞이면서 모양새가 달라져서 금방 중복이 안드러남
  * 어쨋든 문제다, 길이가 늘어나고 알고리즘이 바뀌면 네곳이나 손봐야함
  * `3-7` 에서 include로 중복을 없앤다.

* 결국 많은 원칙과 기법은 중복을 없애거나 제어하려고 나옴

  * 자료에서의 중복 - 관계형 데이터베이스 정규 형식
  * 객체지향 - 코드를 부모클래스로 몰아 중복을 없앤다
  * 구조적 프로그래밍, AOS( Aspect Oriented Programming ), COP (Component Oriented Programming )다 어떤면엣 중복 제거

  

## Structured Programming

* 리턴문이 하나여야한다  - 입구와 출구가 하나만
* 루프 안에서 break / continue는 X
* 함수가 작다면 별 이익을 제공하지 못한다.
  * return, break, continue 를 여러번 써도 된다.



## How Do You Write Functions Like This?

처음부터 탁 하고 짜내지않는다.

길고 복잡하고, 중복된 루프도 많고, 인수도 많고, 

단위 테스트 케이스도 만들고, 코드 다듬고, 함수 만들고, 이름 바꾸고, 중복 제거하고, 메서드 줄이고, 순서 바꾸고, 클래스 쪼개고, 단위테스트 통과하고....



## Conclusion

길이가 짧고 이름이 좋고 체계가 잡힌 함수

시스템이라는 이야기를 풀어가는 게 목표다.



```java
//3-7	
package fitnesse.html;
import fitnesse.responders.run.SuiteResponder; 
import fitnesse.wiki.*;
public class SetupTeardownIncluder { 
  private PageData pageData;
	private boolean isSuite;
	private WikiPage testPage;
	private StringBuffer newPageContent; 
  private PageCrawler pageCrawler;
	public static String render(PageData pageData) throws Exception { 
    return render(pageData, false);
	}
	public static String render(PageData pageData, boolean isSuite) throws Exception {
		return new SetupTeardownIncluder(pageData).render(isSuite);
	}
	private SetupTeardownIncluder(PageData pageData) { 
    this.pageData = pageData;
		testPage = pageData.getWikiPage();
		pageCrawler = testPage.getPageCrawler(); 
    newPageContent = new StringBuffer();
	}
	private String render(boolean isSuite) throws Exception { 
    this.isSuite = isSuite;
		if (isTestPage())
			includeSetupAndTeardownPages(); 
    return pageData.getHtml();
	}
	private boolean isTestPage() throws Exception { 
    return pageData.hasAttribute("Test");
	}
	private void includeSetupAndTeardownPages() throws Exception { 
    includeSetupPages();
		includePageContent();
		includeTeardownPages();
		updatePageContent(); 
  }
  private void includeSetupPages() throws Exception { 
    if (isSuite)
			includeSuiteSetupPage(); 
    includeSetupPage();
	}
  private void includeSuiteSetupPage() throws Exception {
    include(SuiteResponder.SUITE_SETUP_NAME, "-setup");
  }
  private void includeSetupPage() throws Exception { 
    include("SetUp", "-setup");
  }
  private void includePageContent() throws Exception { 
    newPageContent.append(pageData.getContent());
  }
  private void includeTeardownPages() throws Exception { 
    includeTeardownPage();
		if (isSuite)
		  includeSuiteTeardownPage(); 
  }
  private void includeTeardownPage() throws Exception { 
    include("TearDown", "-teardown");
  }
  private void includeSuiteTeardownPage() throws Exception { 
    include(SuiteResponder.SUITE_TEARDOWN_NAME, "-teardown");
  }
  private void updatePageContent() throws Exception { 
    pageData.setContent(newPageContent.toString());
  }
  private void include(String pageName, String arg) throws Exception { 
    WikiPage inheritedPage = findInheritedPage(pageName);
	  if (inheritedPage != null) {
      String pagePathName = getPathNameForPage(inheritedPage);
      buildIncludeDirective(pagePathName, arg); 
    }
  }
  private WikiPage findInheritedPage(String pageName) throws Exception { 
    return PageCrawlerImpl.getInheritedPage(pageName, testPage);
  }
  private String getPathNameForPage(WikiPage page) throws Exception { 
    WikiPagePath pagePath = pageCrawler.getFullPath(page);
	  return PathParser.render(pagePath);
  }
  private void buildIncludeDirective(String pagePathName, String arg) { 
    newPageContent.append("\n!include ").append(arg).append(" .").append(pagePathName).append("\n");
  }
}
```













## 


# Formatting

깔끔하고, 일관적이며, 꼼꼼해야하고, 질서 정연해야한다.

형식을 깔끔하게 맞춰 코드를 짜야하고, 형식을 맞추기 위한 간단한 규칙을 정하고 모두가 그 규칙을 따라야한다.

필요하다면 자동으로 적용하는 도구를 활용한다.

### The Purpose of Formatting

* 코드 형식은 의사소통의 일환, 의사소통은 개발자의 일차적인 의무이다.
* 돌아가는 코드가 일차적인 의무? 아니다.
* 오늘 구현한 기능이 다음 버전에서 바뀔 확률은 아주 높다.
* 오늘 구현한 코드의 가독성은 앞으로 바뀔 코드의 품질에 지대한 영향을 미친다.
* 시간이 지나 흔적을 찾아보기 어려울 정도로 바뀌어도 구현 스타일과 가독성 수준은 유지보수 용이성과 확장에 계속 영향을 미친다.

### Vertical Formatting

* 세로 길이 - 소스 코드는 얼마나 길어야 적당할까?
* 자바에서 파일 크기는 클래스 크기와 밀접하다.
* ![image](https://user-images.githubusercontent.com/72075148/133231454-29fe6b53-19cc-430f-9103-92cd0ad36e94.png)
  * 500줄 안넘어가고 대다수가 200줄 미만의 파일로도 커다란 시스템을 구축 가능하다.

### The Newspaper Metaphor

* 표제를 보고 기사를 읽을지 말지 결정한다, 
* 첫 문단에서 기사 내용을 요약한다.
* 세세한 사실은 숨기고 커다란 그림을 보여준다
* 쭉 읽어 내려가며 세세한 사실이 조금씩 드러난다.
* 기사가 한면을 다 채우진 않지



* 소스코드도 이름은 간단하고 설명이 가능하게 짓는다
* 이름만 보고도 올바른 모듈을 살펴보고 있는지 아닌지를 판단한다.
* 소스 파일 첫 부분은 고차원 개념과 알고리즘을 설명한다
* 아래로 내려갈수록 의도를 세세하게 묘사한다.
* 마지막에는 가장 저차원함수와 세부 내역이 나온다.

## 

### Vertical Openness Between Concepts

* 개념을 빈 행으로 분리해라

* 생각 사이에는 빈 행을 넣어 분리해야 마땅하다.

* ```java
  //5-1
  package fitnesse.wikitext.widgets;
  import java.util.regex.*;
  public class BoldWidget extends ParentWidget {
  	public static final String REGEXP = "'''.+?'''";
  	private static final Pattern pattern = Pattern.compile("'''(.+?)'''",
  		Pattern.MULTILINE + Pattern.DOTALL 
  	);
    
  	public BoldWidget(ParentWidget parent, String text) throws Exception { 
      super(parent);
  		Matcher match = pattern.matcher(text);
  		match.find();
  		addChildWidgets(match.group(1)); 
    }
    
  	public String render() throws Exception { 
      StringBuffer html = new StringBuffer("<b>"); 
      html.append(childHtml()).append("</b>"); 
      return html.toString();
  	} 
  }
  ```

* ```java
  //5-2
  package fitnesse.wikitext.widgets;
  import java.util.regex.*;
  public class BoldWidget extends ParentWidget {
  	public static final String REGEXP = "'''.+?'''";
  	private static final Pattern pattern = Pattern.compile("'''(.+?)'''",
  		Pattern.MULTILINE + Pattern.DOTALL 
  	);
  	public BoldWidget(ParentWidget parent, String text) throws Exception { 
      super(parent);
  		Matcher match = pattern.matcher(text);
  		match.find();
  		addChildWidgets(match.group(1));}
  	public String render() throws Exception { 
      StringBuffer html = new StringBuffer("<b>"); 
      html.append(childHtml()).append("</b>"); 
      return html.toString();
  	} 
  }
  ```



## Vertical Density

* 세로 밀집도

* 줄바꿈이 개념을 분리한다면 세로 밀집도는 연관성을 의미한다.

* 서로 밀접한 코드 행은 세로로 가까이 놓여야 한다는 뜻이다.

* ```java
  public class ReporterConfig {
  	/**
  	* The class name of the reporter listener 
  	*/
  	private String m_className;
  	
  	/	**
  	* The properties of the reporter listener 
  	*/
    private List<Property> m_properties = new ArrayList<Property>();
    public void addProperty(Property property) {
      m_properties.add(property);
    }
  }
  ```

  * 의미없는 주석으로 두 인스턴스 변수를 떨어뜨려놨다.

  ```java
  public class ReporterConfig { 
    private String m_className;
  	private List<Property> m_properties = new ArrayList<Property>();
    
  	public void addProperty(Property property) { 
      m_properties.add(property);
  	}
  }
  ```

### Vertical Distance

* 수직 거리
* 서로 밀접한 개념은 세로로 가까이 둬야한다. - 물론 두 개념이 서로 다른 파일에 속하면 X
* 타당한 근거가 없다면 서로 밀접한 개념은 한 파일에 속해야 마땅하다.
* protected 변수를 피해야 하는 이유중 하나다.

### Variable Declaratioln

* 변수는 사용하는 위치에 최대한 가까이 선언한다. 
* 우리가 만든 함수는 매우 짧으니까 맨 처음에 선언함
* 루프를 제어하는 변수는 흔히 루프 문 내부에 선언한다.
* 드물게 긴 함수에서 블록 상단이나 루프 직전에 선언하는 사례도 있다.



### Instance Variables

* 인스턴스 변수는 클래스 맨 처음에 선언한다, 변수 간에 세로로 거리를 두지 않는다.
* 잘 설계한 클래스는 많은 클래스 메서드가 인스턴스 변수를 사용한다.
* 어디두는지는 논쟁이 분분하다. 어쩃든 잘 알려진 위치에 모아두셈
* 갑자기 이상한데 두면 어려움!

### Dependent Functions

* 한 함수가 다른 함수를 호출하면 두 함수는 세로거리에 가까이 배치

* 가능하면 호출하는 함수를 호출되는 함수보다 먼저 배치한다.

* 그러면 자연스럽게 읽힌다? - 호오>>

* 규칙을 일관적으로 적용한다면 호출한 함수가 잠시 후에 정의되리라는 사실을 예측한다.

* ```java
  public class WikiPageResponder implements SecureResponder { 
    protected WikiPage page;
  	protected PageData pageData;
  	protected String pageTitle;
  	protected Request request; 
    protected PageCrawler crawler;
    
  	public Response makeResponse(FitNesseContext context, Request request) 
      throws Exception {
    	  String pageName = getPageNameOrDefault(request, "FrontPage");
  	  	loadPage(pageName, context); 
      	if (page == null)
  				return notFoundResponse(context, request); 
      	else
  				return makePageResponse(context); 
    }
    
  	private String getPageNameOrDefault(Request request, String defaultPageName) {
  		String pageName = request.getResource(); 
      	if (StringUtil.isBlank(pageName))
  				pageName = defaultPageName;
      
  			return pageName; 
    }
    
    protected void loadPage(String resource, FitNesseContext context) 
      throws Exception {
  		  WikiPagePath path = PathParser.parse(resource);
  		 	crawler = context.root.getPageCrawler(); 
      	crawler.setDeadEndStrategy(new VirtualEnabledPageCrawler()); 
      	page = crawler.getPage(context.root, path);
  	  	if (page != null)
  			  pageData = page.getData();
  	}
    
    private Response notFoundResponse(FitNesseContext context, Request request) 
      throws Exception {
  		  return new NotFoundResponder().makeResponse(context, request);
    }
    
    private SimpleResponse makePageResponse(FitNesseContext context) 
      throws Exception {
      	pageTitle = PathParser.render(crawler.getFullPath(page));
  	    String html = makeHtml(context);
      
  		  SimpleResponse response = new SimpleResponse(); 
      	response.setMaxAge(0); response.setContent(html);
  	 return response;
  	}
    //..
  }
  ```

* 상수를 적절한 수준에 두는 좋은 예제임

  * getPageNameOrDefault 에서 "FrontPage" 상수를 사용하는 방법도 있다.
  * 하지만 기대와 달리 잘 알려진 상수가 적절하지 않은 저차원 함수에 묻힌다. ㅇㅅㅇ?

### Conceptual Affinity

* 개념적인 친화도가 높으면 가까이 배치한다.

* 직접적인 종속성

* 변수와 그 변수를 사용하는 함수

* ```java
  public class Assert {
    static public void assertTrue(String message, boolean condition) {
      if (!condition) fail(message);
    }
    
    static public void assertTrue(boolean condition) { 
      assertTrue(null, condition);
    }
    
    static public void assertFalse(String message, boolean condition) { 
      assertTrue(message, !condition);
    }
    static public void assertFalse(boolean condition) { 
      assertFalse(null, condition);
    }
    //  ...
  ```

  * 명명법이 같다
  * 기본 기능이 유사하다
  * 서로가 서로를 호출하는 부차적인 요인이다.
  * 종속적인 관계가 없더라도 가까이 배치



### Vertical Ordering

* 호출되는 함수를 호출하는 함수보다 나중에 배치한다.
* 고차원에서 저차원으로 자연스럽게 내려간다.



## Horizontal Formatting

* 한 행은 얼마나 길어야할까?
* ![image](https://user-images.githubusercontent.com/72075148/133235161-7d277aa0-c6b8-4f8b-8dbb-8d6a2bc8610b.png)
* 80자 제한은 쫌 인위적이고,
* 100자나 120자도 갠춘하지만 그 이상은 솔직히 주으 ㅣ부족이다.
* 요즘은 모니터가 크니까 ㄱㅊㄱㅊ
* 개인적으로 120자 정도



### Horizontal Openness and Density

공백과 밀집도

밀접한 개념과 느슨한 개념을 표현한다.

```java

private void measureLine(String line) { 
  lineCount++;
	int lineSize = line.length();
	totalChars += lineSize; 
  lineWidthHistogram.addLine(lineSize, lineCount);
  recordWidestLine(lineSize);
}
```

* 할당 연산자를 강조하려고 앞뒤에 공백을 줬다. 왼쪽과 오른쪽 요소가 명백히 나뉨

* 함수 이름과 이어지는 괄호 사이에는 안넣음 - 함수와 인수는 밀접해서

* 쉼표 띄어쓰기로 인수가 별개라는 것을 보여줌

 

```java
public class Quadratic {
  public static double root1(double a, double b, double c) {
		double determinant = determinant(a, b, c);
		return (-b + Math.sqrt(determinant)) / (2*a); 
  }
  
	public static double root2(int a, int b, int c) { 
    double determinant = determinant(a, b, c); r
      eturn (-b - Math.sqrt(determinant)) / (2*a);
	}
	private static double determinant(double a, double b, double c) { 
    return b*b - 4*a*c;
	} 
}

```

* 연산자 우선순위를 강조
* 곱셈은 우선순위가 가장 높다.
* 항 사이에는 공백

### Horizontal Alignment

```java

public class FitNesseExpediter implements ResponseSender {
  private 	Socket 					socket;
  private 	InputStream 		input;
  private 	OutputStream 		output;
  private 	Request 				request;
  private 	Response 				response;
  private 	FitNesseContext context; 
  protected long 						requestParsingTimeLimit; 
  private 	long 						requestProgress; 
  private 	long 						requestParsingDeadline; 
  private 	boolean 				hasError;
}

public FitNesseExpediter(Socket s, 
  FitNesseContext context) throws Exception
{
  this.context = 	context;
  socket = 									s; 
  input = 									s.getInputStream(); 
  output =  								s.getOutputStream(); 
  equestParsingTimeLimit = 	10000;
}

```

* 별로 의미가 없다
* 코드가 엉뚱한 부분을 강조해 진짜 의도가 가려진다.
* 변수 유형은 무시하고 변수 이름부터 읽게 된다.
* 할당 연산자는 안보이고 오른쪽 피 연산자에 눈이 간다.
* IDE 도구는 이거 무시함 ㅋ
* 정렬이 필요할 정도로 목록이 길다면 문제는 목록 길이지 정렬 부족이 아니다.



## Indentation

* 파일 전체에 적용되는 정보가 있고
* 개별 클래스에 적용되는 정보가 있고
* 메서드에 적용되는 정보가 있다.
* 블록 내 블록에 재귀적으로 적용되는 정보가 있다.
* 각 계층에서 각 수준은 이름을 선언하는 범위이자 선언문과 실행문을 해석하는 범위다.

* scope로 이뤄진 계층을 표현하기 위해 우리는 코드를 들여쓴다.



### Breaking Identation

* 간단한 if문, 짧은 while, 짧은 함수에서는 무시하고싶다.

* 하지만 항상 넣는다.

* 뭉뚱그린 코드를 피하자

* ```java
  
  public class CommentWidget extends TextWidget {
  	public static final String REGEXP = "^#[^\r\n]*(?:(?:\r\n)|\n|\r)?";
  	public CommentWidget(ParentWidget parent, String text){super(parent, text);}
  	public String render() throws Exception {return ""; } 
  }
  ```

* 

### Dummy Scopes

* 빈 while문이나 for문
* 빈 블록을 올바로 들여쓰고 괄호로 감싼다.
* while에서 세미 콜론도 꼭 새행에 제대로 들여써서 넣어준다... 눈에안띔 ㅜㅜ



## Team Rules

* 각자 선호하는 규칙이 있겠지만 팀에 속하면 팀규칙을 따라야한다.
* 합의해야한다, 그 규칙을 따라야하고 그래야 일관적이다.




























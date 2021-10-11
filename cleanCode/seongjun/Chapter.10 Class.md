# Classes

* 깨끗한 클래스를 다룸

## Class Organization

* 변수 목록 - 가장 먼저
  * public static 변수
  * private static 변수
  * private instance 변수
  * public 변수가 필요한 경우는 거의 없다.
* 함수 목록
  * public method
  * private method는 자신을 호출하는 public 함수 직후에 넣는다.

### Encapsulation - 캡슐화

* 변수와 유틸리티 함수는 가능한 공개하지 않는다.
* 때론 protected로 선언해 테스트 코드에 접근을 허용함
* 그니까 패키지 전체 공개 혹은 protected ㅇㅇ 하지만 캡슐화를 푸는건 최후의 수단

### Classes Should Be Small!

* 첫 번째 규칙 - 작아야함
* 두 번째 규칙 - 작아야함
* 함수는 물리적인 행 수로 크기를 측정했다면 클래스는 책임으로 센다.

```java
//10-1
public class SuperDashboard extends JFrame implements MetaDataUser 
  public String getCustomizerLanguagePath()
	public void setSystemConfigPath(String systemConfigPath) 
  public String getSystemConfigDocument()
	public void setSystemConfigDocument(String systemConfigDocument) 
  public boolean getGuruState()
	public boolean getNoviceState()
	public boolean getOpenSourceState()
	public void showObject(MetaObject object) 
  public void showProgress(String s)
  ..
  // + .. 짱많음
```

```java
//10-2
public class SuperDashboard extends JFrame implements MetaDataUser 
  public Component getLastFocusedComponent()
	public void setLastFocused(Component lastFocused)
	public int getMajorVersionNumber()
	public int getMinorVersionNumber()
	public int getBuildNumber() 
  }
```

* 다섯 개 정도면 갠춘하지않나? 
* 아님 SuperDashboard는 메서드 수가 작지만 책임이 너무 많다.
* 클래스 이름은 해당 클래스 책임을 기술해야 한다.
* 작명은 클래스 크기를 줄이는 첫 번째 관문이다. 
  * 만약 이름이 안떠오르면 클래스가 너무 큰거다.
  * 모호하면 책임이 너무 많아서이다.
* Processor / Manager / Super 처럼 모호한 단어가 있다면 클래스에다 여러 책임을 안겼다는 증거
* if / and / or / but 을 쓰지않고 25단어 내외로 설명이 가능해야함
  * "The SuperDashboard provides access to the component that last held the focus, and it also allows us to track the version and build number"
  * and ~ 는 너무 책임이 많다는 증거

### The Single Responsibility Principle - 단일 책임 원칙

* 클래스나 모듈을 변경할 이유가 하나 뿐이여야한다.
* SRP는 책임이라는 개념을 정의하고 적절한 크기의 클래스를 제시함
* `10-2` 는 변경할 이유가 두 가지이다.
  * 소프트웨어 버전 정보를 추적한다. - 버전 정보는 소프트웨어를 출시할 때 마다 달라진다.
  * 자바 스윙 컴포넌트를 관리한다. 그때마다 버전 번호를 바꾼다.

```java
public class Version {
	public int getMajorVersionNumber() 
  public int getMinorVersionNumber() 
  public int getBuildNumber()
}
```

* 책임. 즉 변경할 이유를 파악하려 애쓰다 보면 코드를 추상화하기도 쉬워진다.
* 객체지향에서 중요한 개념이지만 가장 무시하는 규칙 중 하나.
* 우리는 깨끗하고 체계적인 소프트웨어 보다 돌아가는 소프트웨어에 초점을 맞춘다.
* 뭐 중요하다 .. 또강조 잘 정리해서 .. 해야한다..

### Cohesion

* 인스턴스 변수 수가 작아야한다.
* 각 클래스 메서드는 클래스 인스턴스 변수를 하나 이상 사용해야한다.
* 메서드가 변수를 더 많이 사용할수록 메서드와 클래스의 응집도가 더 높다.
* 모든 인스턴스 변수를 메서드마다 사용하는 클래스는 응집도가 가장 높다.

```java
public class Stack {
	private int topOfStack = 0;
	List<Integer> elements = new LinkedList<Integer>();
	public int size() { 
    return topOfStack;
  }
	public void push(int element) { 
    topOfStack++; elements.add(element);
  }
	public int pop() throws PoppedWhenEmpty { 
    if (topOfStack == 0)
			throw new PoppedWhenEmpty();	
		int element = elements.get(--topOfStack); elements.remove(topOfStack);
		return element;
	} 
}
```

* 함수를 작게, 매개변수 목록을 짧게 를 하다보면 인스턴스 변수가 아주 많아진다.
* 새로운 클래스로 쪼개라는 신호임
* 응집도가 높아지도록 변수와 메서드를 적절히 분리해서 새로운 클래스 두세 개로 쪼개준다.

### Maintaining Cohesion Results in Many Small Classes

* 큰 함수를 작은 함수 여럿으로 나누기만 해도 클래스 수가 많아진다.
* 변수가 많은 큰 함수가 하나 있다?
* 큰 함수 일부를 작은 함수 하나로 빼내고싶은데, 빼내려는 코드가 큰 함수에 정의된 변수 넷을 사용한다.
* 그럼 인수로 넘기나? - ㄴㄴ 아님 네 변수를 클래스 인스턴스 변수로 승격하면 새 함수는 인수가 필요없음
* 이렇게 하면 응집력을 잃는다.. 몇몇 함수만 사용하는 인스턴수 변수가 점점 늘어난다..
* 근데 몇몇 함수가 몇몇 변수만 사용하면 독자적인 클래스로 분리해도 되는거 아냐? - 응집력을 잃는다면 쪼개라.

```java
//10-5
package literatePrimes;
public class PrintPrimes {
public static void main(String[] args) {
  final int M = 1000; final int RR = 50;
  final int CC = 4;
  final int WW = 10;
  final int ORDMAX = 30; 
  int P[] = new int[M + 1]; 
  int PAGENUMBER;
  int PAGEOFFSET; 
  int ROWOFFSET; 
  int C;
  int J;
  int K;
  boolean JPRIME;
  int ORD;
  int SQUARE;
  int N;
  int MULT[] = new int[ORDMAX + 1];
  J = 1;
  K = 1; 
  P[1] = 2; 
  ORD = 2; 
  SQUARE = 9;
  while (K < M) { 
    do {
		  J = J + 2;
    	if (J == SQUARE) {
			  ORD = ORD + 1;
			  SQUARE = P[ORD] * P[ORD]; 
        MULT[ORD - 1] = J;
		  }
	  N = 2;
	  JPRIME = true;
	  while (N < ORD && JPRIME) {
  		while (MULT[N] < J) 
        MULT[N] = MULT[N] + P[N] + P[N];
		  if (MULT[N] == J) 
        JPRIME = false;
		  N = N + 1; 
    }
  } while (!JPRIME); 
    K = K + 1;
	  P[K] = J;
  } {
    PAGENUMBER = 1;
    PAGEOFFSET = 1;
    while (PAGEOFFSET <= M) {
      System.out.println("The First " + M + 
        " Prime Numbers --- Page " + PAGENUMBER);
      System.out.println("");
      for (ROWOFFSET = PAGEOFFSET; ROWOFFSET < PAGEOFFSET + RR; ROWOFFSET++){
        for (C = 0; C < CC;C++)
          if (ROWOFFSET + C * RR <= M)
            System.out.format("%10d", P[ROWOFFSET + C * RR]); 
        System.out.println("");
      }
      System.out.println("\f"); 
      PAGENUMBER = PAGENUMBER + 1; 
      PAGEOFFSET = PAGEOFFSET + RR * CC;
      }
    }
  }
}
```

* 들여쓰기가 심하고, 이상한 변수가 많고, 구조가 빡세게 결합되어있음
* 여러 함수로 나눠야함

```java
// 10-6 PrimePrinter.java
package literatePrimes;
public class PrimePrinter {
	public static void main(String[] args) {
		final int NUMBER_OF_PRIMES = 1000;
		int[] primes = PrimeGenerator.generate(NUMBER_OF_PRIMES);
		final int ROWS_PER_PAGE = 50; 
    final int COLUMNS_PER_PAGE = 4; 
    RowColumnPagePrinter tablePrinter =  new RowColumnPagePrinter(ROWS_PER_PAGE,
                                                                  COLUMNS_PER_PAGE,
                                                                  "The First " + 
                                                                  NUMBER_OF_PRIMES + 
                                                                  " Prime Numbers");
		tablePrinter.print(primes); 
  }
}
```
```java
//10-7 RowColumnPagePrinter.java
package literatePrimes;
import java.io.PrintStream;
public class RowColumnPagePrinter { 
  private int rowsPerPage;
	private int columnsPerPage; 
  private int numbersPerPage; 
  private String pageHeader; 
  private PrintStream printStream;
	public RowColumnPagePrinter(int rowsPerPage, int columnsPerPage, String pageHeader) {
    this.rowsPerPage = rowsPerPage;
    this.columnsPerPage = columnsPerPage; 
    this.pageHeader = pageHeader;
		numbersPerPage = rowsPerPage * columnsPerPage; 
    printStream = System.out;
	}
  public void print(int data[]) { 
    int pageNumber = 1;
    for (int firstIndexOnPage = 0; firstIndexOnPage < data.length; firstIndexOnPage += numbersPerPage) { 
      int lastIndexOnPage = Math.min(firstIndexOnPage + numbersPerPage - 1, data.length - 1);
      printPageHeader(pageHeader, pageNumber); 
      printPage(firstIndexOnPage, lastIndexOnPage, data); 
      printStream.println("\f");
      pageNumber++;
    } 
  }

  private void printPage(int firstIndexOnPage, int lastIndexOnPage, int[] data) { 
    int firstIndexOfLastRowOnPage = firstIndexOnPage + rowsPerPage - 1;
    for (int firstIndexInRow = firstIndexOnPage; firstIndexInRow <= firstIndexOfLastRowOnPage; firstIndexInRow++) { 
      printRow(firstIndexInRow, lastIndexOnPage, data);
      printStream.println("");
    } 
  }

  private void printRow(int firstIndexInRow, int lastIndexOnPage, int[] data) {
    for (int column = 0; column < columnsPerPage; column++) {
      int index = firstIndexInRow + column * rowsPerPage; 
      if (index <= lastIndexOnPage)
        printStream.format("%10d", data[index]); 
    }
  }

  private void printPageHeader(String pageHeader, int pageNumber) {
    printStream.println(pageHeader + " --- Page " + pageNumber);
    printStream.println(""); 
  }
	public void setOutput(PrintStream printStream) { 
  	this.printStream = printStream;
	} 
}
```



```java
//10-8 PrimeGenerator.java
package literatePrimes;
import java.util.ArrayList;
public class PrimeGenerator {
	private static int[] primes;
	private static ArrayList<Integer> multiplesOfPrimeFactors;
	protected static int[] generate(int n) {
		primes = new int[n];
		multiplesOfPrimeFactors = new ArrayList<Integer>(); 
    set2AsFirstPrime(); 
    checkOddNumbersForSubsequentPrimes();
		return primes; 
  }
	private static void set2AsFirstPrime() { 
    primes[0] = 2; 
    multiplesOfPrimeFactors.add(2);
	}
	private static void checkOddNumbersForSubsequentPrimes() {
    int primeIndex = 1;
		for (int candidate = 3; primeIndex < primes.length; candidate += 2) { 
      if (isPrime(candidate))
				primes[primeIndex++] = candidate; 
    }
	}
  private static boolean isPrime(int candidate) {
		if (isLeastRelevantMultipleOfNextLargerPrimeFactor(candidate)) {
			multiplesOfPrimeFactors.add(candidate);
			return false; 
    }
		return isNotMultipleOfAnyPreviousPrimeFactor(candidate); 
  }
  
  private static boolean isLeastRelevantMultipleOfNextLargerPrimeFactor(int candidate) {
    int nextLargerPrimeFactor = primes[multiplesOfPrimeFactors.size()];
    int leastRelevantMultiple = nextLargerPrimeFactor * nextLargerPrimeFactor; 
    return candidate == leastRelevantMultiple;
  }
  
  private static boolean isNotMultipleOfAnyPreviousPrimeFactor(int candidate) {
		for (int n = 1; n < multiplesOfPrimeFactors.size(); n++) {
			if (isMultipleOfNthPrimeFactor(candidate, n)) 
        return false;
    }
    return true; 
  }
  
  private static boolean isMultipleOfNthPrimeFactor(int candidate, int n) {
		return
			candidate == smallestOddNthMultipleNotLessThanCandidate(candidate, n);
	}
	private static int smallestOddNthMultipleNotLessThanCandidate(int candidate, int n) {
		int multiple = multiplesOfPrimeFactors.get(n); 
    while (multiple < candidate)
      multiple += 2 * primes[n]; 
    multiplesOfPrimeFactors.set(n, multiple); 
    return multiple;
}
  
```

* 길어졌지, 거의 세페이지
  * 리펙터링한 프로그램을 길고 서술적인 변수 이름 사용
  * 주석을 추가하는 수단으로 함수 선안과 클래스 선언을 활용
  * 공백을 추가하고 형식을 맞춤

* 원래는 세 가지 책임을 졌다.
  * PrimePrinter 클래스는 main 함수 하나만 포함하며 실행 환경을 책임진다.
    * 호출 방식이 달라지면 그 클래스가 바뀜
  * RowColumnPagePrinter 클래스는 숫자 목록을 주어진 행과 열에 맞춰 페이지에 출력하는 방법을 안다. 
    * 출력하는 모양을 바꾸려면 RowColumnPagePrinter 클래스를 바꿔준다.
  * PrimeGenerator 클래스는 소수 목록을 생성하는 방법을 안다.
    * 객체로 인스턴흐화 하는 클래스가 아니다.
    * 단순 변수를 선언하고 감추려고 사용하는 유용한 공간 뿐 , 알고리즘 바뀌면 이걸 고친다.
* 재구현이 아니다, 프로그램을 처음부터 다시 짜지 않았다. 원리는 동일함
* 원래 프로그램의 정확한 동작을 검증하는 test suite를 작성했다. 그런 다음 한 번에 하나씩 수 차례에 걸쳐 조금씩 변경

## Organizing for Change

* 보통 시스템은 지속적으로 변경해야하는데 , 변경할 때마다 의도대로 동작 안할 위험.. 체계적으로 정리해 변경에 수반하는 위험 낮추자

* ```java
  //10-9
  public class Sql {
    public Sql(String table, Column[] columns)
    public String create()
    public String insert(Object[] fields)
    public String selectAll()
    public String findByKey(String keyColumn, String keyValue)
    public String select(Column column, String pattern)
    public String select(Criteria criteria)
    public String preparedInsert()
    private String columnList(Column[] columns)
    private String valuesList(Object[] fields, final Column[] columns) 
    private String selectWithCriteria(String criteria)
    private String placeholderList(Column[] columns)
  }
  ```

* update문을 지원해야 하면 클래스에 손대어 고쳐야함

* 기존 sql 수정하려면 손대야함

  * 이래서 ... srp 위반이라고??

* `selectWithCriteria` 는 select문을 처리할때만 사용한다.

  * 클래스 일부에서만 사용되는 비공개 메서드는 코드를 개선할 잠재적인 여지

* sql클래스가 논리적으로 완성이라 생각한다면 분리할 시도X

* 가까운 장래에 Update 필요없다면 뭐,.

```java
//   Listing 10-10
//A set of closed classes
abstract public class Sql {
		public Sql(String table, Column[] columns) 
    abstract public String generate();
}

public class CreateSql extends Sql {
		public CreateSql(String table, Column[] columns) 
    @Override public String generate()
}

public class SelectSql extends Sql {
		public SelectSql(String table, Column[] columns) 
    @Override public String generate()
}

public class InsertSql extends Sql {
	public InsertSql(String table, Column[] columns, Object[] fields) 
  @Override public String generate()
	private String valuesList(Object[] fields, final Column[] columns)
}

public class SelectWithCriteriaSql extends Sql { 
  public SelectWithCriteriaSql(String table, Column[] columns, Criteria criteria) 
  @Override public String generate()
}

public class SelectWithMatchSql extends Sql { 
  public SelectWithMatchSql(String table, Column[] columns, Column column, String pattern)
  @Override public String generate()
}

public class FindByKeySql extends Sql {
	 public FindByKeySql(String table, Column[] columns, String keyColumn, String keyValue)
   @Override public String generate()
}


public class PreparedInsertSql extends Sql {
	public PreparedInsertSql(String table, Column[] columns) 
  @Override public String generate() {
		private String placeholderList(Column[] columns)
	}
}
  
public class Where {
	public Where(String criteria) 
  public String generate()
}

public class ColumnList {
		public ColumnList(Column[] columns) 
    public String generate()
}

```

* 함수 하나 수정한다고 다른 함수 망가질 위험도 사라짐
* 테스트 관점에서 모든 논리를 구석구석 증명하기 쉬움
* update 추가한다고 기존 클래스 변경 안해도됨
* SRP를 지원한다.

## Isolation from Change

* 요구사항은 변경되며 코드도 변한다.

* 상세한 구현에 의존하는 클라이언트 클래스는 구현이 바뀌면 위험에 빠진다.

* 인터페이스와 추상 클래스를 사용해 구현이 미치는 영향을 격리한다.

* Portfolio클래스를 만든다고 가정

  * TokyoStockExchange API를 통해 포트폴리오 값을 계산한다.

  * 테스트코드가 시세 변화에 영향을 받음 ;;

  * StockExchange라는 인터페이스 생성 후 메서드를 선언

  * ```java
    public interface StockExchange { 
      Money currentPrice(String symbol);
    }
    ```

  * StockExchange를 구현하는 TokyoStackExchange를 구현

  * Portfolio를 수정해 StockExchange참조자를 인수로 

  * ```java
    public Portfolio {
    	private StockExchange exchange;
    	public Portfolio(StockExchange exchange) {
    		this.exchange = exchange; 
      }
    // ... 
    }
    ```

  * TokyouStockExchange를 흉내내는 테스트용 클래스를 만들 수 있다.

  * 인터페이스 구현하고, 고정된 주가를 반환한다. 

  * ```java
    public class PortfolioTest {
    	private FixedStockExchangeStub exchange; 
      private Portfolio portfolio;
      
    	@Before
    	protected void setUp() throws Exception {
    		exchange = new FixedStockExchangeStub(); 
        exchange.fix("MSFT", 100);
    		portfolio = new Portfolio(exchange);
    	}
      
    	@Test
    	public void GivenFiveMSFTTotalShouldBe500() throws Exception {
    		portfolio.add(5, "MSFT");
    		Assert.assertEquals(500, portfolio.value()); 
      }
    }
    ```

  * 시스템의 결합도를 낮추면 유연성과 재사용성도 높아진다.

  * 결합도가 낮다는건 각 시스템 요소가 서로 변경으로부터 잘 격리 되어있다는것 

  * 격리되어있으면 이해도 쉬움

  * 결합도를 낮추면 DIP를 따르는 클래스가 나온다 Dependency Inversion Principle

  * 상세한 구현이 아닌 추상화에 의존하라
  
  


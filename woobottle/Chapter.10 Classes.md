# 10. Classes

### 클래스 체계
표준 자바 관례에서는
변수 목록이 나온다
1. 정적 공개 상수
2. 정적 비공개 상수
3. 비공개 인스턴스 변수

공개 함수가 다음으로 나온다.
비공개 함수는 자신을 호출하는 공개 함수 직후에 넣는다. 즉 추상화 단계가 순차적으로 내려간다.
그래서 신문 기사처럼 읽힌다.

* 캡슐화
때로는 변수나 유틸리티 함수를 protected로 선언해 테스트 코드에 접근을 허용하기도 한다.
-> case by case 인것 같다.
하지만 이것은 제일 나중의 방법이다.

### 클래스는 작아야 한다.
클래스는 무조건 작아야 한다.
클래스는 맡은 책임으로 센다. 행 수로 크기를 측정하는 것이 아니다.
-> 클래스 별로 꼭 필요한 기능들만 가지고 있어야 한다는 이야기 인것 같다.

```java
  public class SuperDashboard extends JFrame implements MetaDataUser {
    public Component getLastFocusedComponent();
    public void setLastFocused(Component lastFocused)
    public int getMajorVersionNumber()
    public int getMinorVersionNumber()
    public int getBuildNumber()
  }
```

위의 클래스도 크기가 너무크다. 단어는 25단어 내외로 가능해야 하며
이름이 잘 떠오르지 않는다면 클래스 크기가 너무 커서다

### 단일 책임 원칙
-> 클래스나 모듈을 변경할 이유가 하나뿐이어야 한다. (Solid원칙중의 하나)
위의 superdashboard 클래스를 변경해야하는 이유는 두 가지다
1. 버전 정보는 바뀔수가 있다.
2. 자바 스윙 컴포넌트를 관리한다???(스윙 코드를 변경할 때마다 버전 번호가 바뀐다)

```java
  // superDashboard에서 version 클래스를 빼서 만들어 준다
  public class Version {
    public int getMajorVersionNumber()
    public int getMinorVersionNumber()
    public int getBuildNumber()
  }
```

소프트웨어를 돌아가게 만드는 활동과 소프트웨어를 깨끗하게 만드는 활동은 완전히 별개다
적절한 비유 => 도구상자를 어떻게 관리하고 싶은가? 작은 서랍을 많이 두고 기능과 이름이 명확한 컴포넌트를 나눠 넣고 싶은가? 아니면 큰 서랍 몇개를 두고 모두를 던져 넣고 싶은가?

큰 클래스 몇개가 아니라 작은 클래스 여럿으로 이뤄진 시스템이 더 바람직하다.

### 응집도
각 클래스 메서드는 클래스 인스턴스 변수를 하나 이상 사용해야 한다.
메서드가 클래스 변수를 더 많이 사용할수록 메서드와 클래스는 응집도가 더 높다
모든 인스턴스 변수를 메서드마다 사용하는 클래스는 응집도가 가장 높다.

응집도가 높다는 말 => 클래스에 속한 메서드와 변수가 서로 의존하며 논리적인 단위로 묶인다

```java
  // 응집도가 높은 클래스
  public class Stack {
    private int topOfStack = 0;
    List<Integer> elements = new LinkedList<Integer>();

    public int size() {
      return topOfStack;
    }

    public void push(int element) {
      topOfStack++;
      elements.add(element);
    }

    public int pop() throws PoppedWhenEmpty {
      if (topOfStack == 0) {
        throw new PoppedWhenEmpty();
      }
      int element = elements.get(--topOfStack);
      elements.remove(topOfStack);
      return element;
    }
  }

  // 메서드마다 클래스 변수를 모두 사용하는것이 응집도가 높다.
  // size를 제외한 모든 메서드가 두개의 변수를 다 사용한다.
```

### 응집도를 유지하면 작은 클래스 여럿이 나온다
큰 함수를 작은 함수 여럿으로 나눈다
변수가 아주 많은 큰 함수 
-> 작은 함수로 빼고 싶은데 이 함수가 큰 함수에 정의된 변수 넷을 사용한다 
-> 변수 네개를 클래스 변수로 빼버린다. 이러면 작은함수에 넘길 인자는 없다 
-> 이렇게 하면 몇몇의 메서드만이 사용하는 클래스 변수가 너무 많아진다.(응집도가 약해진다)
-> 몇몇 함수가 몇몇 변수만 사용한다면 독자적인 클래스로 분리해버린다.

```java
// 리팩토링이 필요한 코드
package literalPrimes;

public class PrintPrimes {
  public static void main(String[] args) {
    final int M = 1000;
    final int RR = 50;
    final int CC = 4;
    final int WW = 10;
    final int ORDMAX = 30;
    int P[] = new int[M +1];
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
          while (MULT[N] < J) {
            MULT[N] = MULT[N] + P[N] + P[N];
          }
          if (MULT[N] == J) {
            JPRIME = false;
          }
          N = N + 1;
        }
      } while (!JPRIME);
      K = K + 1;
      P[K] = J;
    }
    {
      PAGENUMBER = 1;
      PAGEOFFSET = 1;
      while (PAGEOFFSET <= M) {
        System.out.prinln("The First " + M + " Prime Numbers --- Page " + PAGENUMBER);
        System.out.println("");
        for (ROWOFFSET = PAGEOFFSET; ROWOFFSET < PAGEOFFSET + PR; ROWOFFSET++) {
          for (C = 0; C < CC; C++) {
            if (ROWOFFSET + C * RR <= M) {
              System.out.format("%10d", P[ROWOFFSET + C * PR]);
            }
            System.out.println("");
          }
        }
        System.out.println("\f");
        PAGENUMBER = PAGENUMBER + 1;
        PAGEOFFSET = PAGEOFFSET + PR * CC;
      }
    } 
  }
}
```


### 변경하기 쉬운 클래스

```java
public class Sql {
  public Sql(String table, Column[] columns)
  public String create()
  public String insert(Object[] fields)
  public String selectAll()
  public String findByKey(String keyColumn, String keyValue)
  public String select(Column column, String pattern)
  public String selct(Criteria criteria)
  public String preparedInsert()
  private String columnList(Column[] columns)
  private String valuesList(Object[] fields, final Column[] columns)
  private String selectWithCriteria(String criteria)
  private String placeholderList(Column[] columns)
}
```

위의 클래스는 변경하여야 할 이유가 두가지다.
1. 기존의 sql문을 수정해야할때,
2. 새로운 sql문을 지원하려면 

위의 코드에 있던 공개 인터페이스를 각각 Sql 클래스에서 파생하는 클래스로 생성
private 메서드들은 파생 클래스로 옮김
모든 파생 클래스가 공통으로 사용하는 비공개 메서드는 Where와 ColumnList라는 두 유틸리티 클래스로 넣었다 -> 뭔소리야?? -> select하려면 where와 칼럼리스트는 필수

```java
// 닫힌 클래스 집합
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

public class FindByKeySql extends Sql {
  public FindByKeySql(String table, Column[] columns, String keyColumn, String keyValue)
  @Override public String generate()
}

public class PreparedInsertSql extends Sql {
  public PreparedInsertSql(String table, Column[] columns)
  @Override public String generate()
  private String placeholderList(Column[] columns)
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

### 변경으로부터 격리
-> 5분마다 변경되는 api값에 대응하기 위해 테스트 하는 방법의 예시

상세한 구현에 의존하는 클라이언트 클래스는 구현이 바뀌면 위험에 빠진다.
그래서 우리는 인터페이스와 추상 클래스를 사용해 구현이 미치는 영향을 격리한다.


상세한 구현에 의존하는 코드는 테스트가 어렵다. 그래서 아래의 예시에서는 테스트 코드에서 고정값을 반환하게 해서 테스트 한다.
```java
public interface StockExchange {
  Money currentPrice(String symbol);
}

public Portfolio {
  private StockExchange exchange;
  public Portfolio(StockExchange exchange) {
    this.exchange = exchange;
  }
}

public class PortfolioTest {
  private FixedStockExchangeStub exchange;
  private Portfolio portfolio;

  @Before
  protected void setUp() throws Exception {
    exchange = new FixedStockExchangeStub();
    exchange.fix("MSFT", 100);
    portfolio = new PortFolio(exchange);
  }

  @Test
  public void GivenFiveMSFTTotalShouldBe500() throws Exception {
    portfolio.add(5, "MSFT");
    Assert.assertEquals(500, portfolio.value());
  }
}
```

DIP(Dependency Inversion Principle)
-> 클래스가 상세한 구현이 아니라 추상화에 의존해야 한다는 원칙!!!
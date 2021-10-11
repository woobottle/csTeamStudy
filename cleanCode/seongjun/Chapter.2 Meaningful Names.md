# 2. Meaningful Names

### Use Intention-Revealing Names

의도가 분명하게 이름을 지어... 말이쉽지

좋은 이름으로 지으려면 시간이 걸리지만 그만만큼 절약하는 시간이 훨씬 더 많다.

```java
int d;
//vs
int elapsedTimeInDays;
int daysSinceCreateion;
int daysSinceModification;
int fileAgeIndays;

public List<int[]> getThem(){
  List<int[]> list1 = new ArrayList<int[]>();
  for (int[] x : theList)
    if(x[0] == 4)
      list1.add(x);
  return list1;
}
```

1. theList에 무엇이 들었나?
2. 0번째가 왜 중요한가
3. 4는 무슨의미인가
4. 반환하는 함수는 뭘 의미하나 

를 안다고 가정하고 작성되어있다.



만약 지뢰찾기 게임을 만든다고 가정한다.

theList는 게임판이다. 0번째는 칸 상태를 뜻하고, 값 4는 깃발이 꽂힌 상태를 의미한다.

```java
public List<int[]> getFlaggedCells(){
  List<int[]> flaggedCless = new ArrayList<int[]>();
  for(int[] cell: gameBoard)
    if(cell[STATUS_VALUE] == FLAGGED)
      flaggedCells.add(cell);
  return flaggedCells;
}

public List<Cell> getFlaggedCells(){
  List<Cell> flaggedCless = new ArrayList<Cell>();
  for(Cell cell: gameBoard)
    if(cell[STATUS_VALUE] == FLAGGED)
      flaggedCells.add(cell);
  return flaggedCells;
}
```



### Avoid Disinformation

* hp/ aix/ sco는 변수 이름으로 적합하지 않다, 유닉스 플랫폼이나 유닉스 변종을 가리키는 이름이라서

* 그룹으로 묶을 때 List가 아니라면 accountList 라 명명하지 않는다.
  * accountGroup / bunchOfAccounts , accounts 등으로 명명

* 서로 흡사한 이름을 사용하지 않도록한다.
  * XYZControllerForEfficientHandlingOfStrings , XYZControllerForEfficientStorageOfStrings
* 유사한 개념은 유사한 표기법을 사용한다., 일관성이 떨어지는 표기법은 그릇된 정보다.

### Make Meaningful Distinctions - 의미 있게 구분하라

* 연속적으로 숫자를 덧붙인 이름은 아무런 정보를 제공하지 못하는 이름이다, - a1, a2
* source / destination을 사용하면 코드 읽기가 훨씬 더 쉬워진다.
* 불용어를 추가한 이름도 아무런 정보를 제공하지 못한다. Product . - ProductInfo / ProductData 
  * 개념을 구분하지 않은 채 이름만 달리한 경우다. a, an, the처럼 불분명한 불용어이다.
  * 접두어를 아예 쓰지말란건 아니고 zork 변수가 있다고 theZork을 쓰는건 에바라는거
* 불용어는 중복이다. 변수 이름에 variable 이라는 단어를 쓰지마라, 표에 table을 쓰지마라, NameString - Name
* Customer - CustomerObject /  getActiveAccount() - getActiveAccounts()  - getActiveAccountInfo() 
* customerInfo - customer / accountData - account / theMessage - message
* 구분이 안된다. 읽는 사람이 차이를 알도록 이름을 지어라

### Use Pronounceable Names

`genymdhms`, ` modymdhms`

generationTimeStamp, modificationTimestamp;

### Use Searchable Names

* 문자 하나를 사용하는 이름과, 상수는 텍스트 코드에서 쉽게 눈에 띄지 않는다.
* `MAX_CLASSES_PER_STUDENT` 는 찾기 쉽지만 7은 찾기 어렵다.

```java
for(int j=0; j<34; j++){
  s += (t[j]*4)/5;
}


int realdaysPerIdealDay = 4;
const int WORK_DAYS_PER_WEEK = 5;
int sum = 0 ;
for(int j=0; j < NUMBER_OF_TASKS; j++){
  int realTaskDays = taskEstimate[j] * realDaysPerIdealDay;
  int realTaskWeeks = (realTaskDays/WORK_DAYS_PER_WEEK);
  sum += realTaskWeeks;
}
```



### Avoid Encoding

#### Hungarian Notation

옛날 컴팡일러는 타입 체크를 안해서 타입을 기억할 단서가 필요했다. 요즘은 변수이름에 타입을 인코딩 할 필요가 없다.

객체는 강한 타입이고 IDE는 컴파일하지 않고도 타입 오류를 감지할 수 있다.

오히려 방해가 되고 변수 함수 클래스이름이나 타입을 바꾸기가 어려워지고 읽기도 어려워진다.

#### Member Prefixes

멤버 변수엥 m_ 이라는 접두어를 붙일 필요가 없다. 어차피 IDE에서 색으로 따로 표시해줄거임

### Interfaces and Implementations

도형을 생성하는 ABSTRACT FACTORY를 구현한다고 가정, 인터페이스 클래스이고, 구현은 concrete class에서 한다.

이 두 클래스 이름을 어떻게 지어야할까?

'I' prefix는, 주의를 흐트리고 과도한 정보를 제공한다.

인터페이스라는 사실을 남에게 알리고 싶지 않다...?

클래스 사용자는 그냥 ShapeFactory 라고만 생각하면 좋겠다.. 인코딩 한다는 구현 클래스 이름을 선택한다

ShapeFactoryImp나 CShapeFactory 가 IShapeFactory보다 좋다...??

### Avoid Mental Mapping

* i, j, k 정돈 뭐.. (l 은 절대안댐 ) 단 루프 범위가 작고 다른이름고 충돌하지 않을 때만 괜찮다.
* r이라는 변수가 호스트와 프로토콜을 제외한 소문자 url이라는 사실을 언제나 기억한다면.... 똑똑하지만 .... 

### Class Names

* 클래스 이름과 객체 이름은 명사나 명사구가 적합하다.
* 좋 - Customer, WikiPage, Account, AddressParser
* 나쁨 - Manager, Processor, Data, Info 같은 단어나, 동사는 사용하지 않음

### Method Names

* 메서드는 동사나 동사구가 적합하다. postPayment, deletePage, save 등
* Accesor, Mutator, Predicate는 get, set, is를 붙인다.
* 생성자를 overload할 때는 정적 팩토리 메서드를 사용 - 아셈?
  * 메서드는 인수를 설명하는 이름을 사용한다.

```java
// 이게낫다임
Complex fulcrumPoint = Complex.FromRealNumber(23.0);

//이거보단 ..
Complex fulcrumPoint = new Complex(23.0);

```

생성자 사용을 제한하려면 해당 생성자를 privated으로 선언한다



### Don't Be Cute

HolyHandGrenade...... 보단 DeleteItems

### Pick One Word Per Concept

* 추상적인 개념 하나에 단어 하나를 선택해서 고수한다.

* fetch / retrieve / get 으로 제각각이면 혼란스럽다.

* 이른은 독자적이고 일관적이여야한다.

### Don't Pun

* 한 단어를 두가지 목적으로 사용하지 마라

* 여러 클래스에 똑같은 add 라는 메서드를 쓴다?

* 모두 똑같은 역할을 한다면 모를까, 새로 작성하는 메서드는 집합에 값을 하나를 추가하는거라면 맥락이 다르다. insert / append 가 적당하다.

### Use Solution Domain Names

* 코드를 읽는 사람도 프로그래머이다, 전산용어, 알고리즘 이름, 패턴이름, 수학용어를 써도 된다.
* Visitor패턴 , JobQueue, 등..

### Use Problem Domain Names

* 적절한 프로그래머 용어가 없으면 도메인 영역에서 이름을 갖고온다.

### Add Meaningful Context

* 의미가 분명한 이름이 없지 않다 하지만 대다수 이름은 그렇지 못함
* classes, functions, namespaces에 넣어 맥락을 부여한다.
* 모든 방법이 실패하면 마지막 수단으로 접두어를 붙인다.

firstName, lastName, Street, houseNumber, city, state, zipcode

주소란걸 알아차리기 쉽지만 state만 쓴다면 알기 어렵다?

addrFirstName, addrLastName, addrState라 쓰면 좀더 분명해진다.

물론 Address라는 클래스를 생성하면 더 좋음

```java
private void printGuessStatistics(char candidate, int count){
  String number;
  String verb;
  String pluralModifier;
  if(count == 0 ){
    number = 'no';
    verb = 'are';
    pluralModifier = 's';
  }else if (count == 1){
    number = '1';
    verb = 'is';
    pluralModifier = '';
  }else{
    number = Integer.toString(count);
    verb = 'are';
    pluralModifier = 's';
  }
  String guessMessage = String.format(
	  "There %s %s %s%s", verb, number, candidate, pluralModifier
    );
  print(guessMessage);
}
```

* 함수 이름은 맥락의 일부만 제공하고, 알고리즘이 나머지 맥락을 제공한다.
* 끝까지 읽어보고 나서야 알 수 있음.

일단 함수가 좀 길고, 세 변수를 함수 전반에서 사용한다.

GuessStatisticsMessage라는 클래스를 만들고, 세 변수를 클래스에 넣어 함수를 작은 조각으로 쪼갠다.

```java
public class GuessStatisticsMessage{
  private String number;
  private String verb;
  private String pluralModifier;
  public String make(char candidate, int count){
    createPluralDependentMessagePart(count);
    return String.format(
      "There %s %s %s%s", verb, number, candidate, pluralModifier
    );
  }
  public void createPluralDependentMessageParts(int count){
    if(count == 0){
      thereAreNoLetters();
    }else if(count == 1){
      thereIsOneLetter();
    }else{
      thereAreManyLetters(count);
    }
  }
  
  private void thereAreManyLetters(int count){
    number = Integer.toString(count);
    verb="are";
    pluralModifier = "s";
  }
  private void thereIsOneLetter(int count){
    number = "1";
    verb="is";
    pluralModifier = "";
  }
  private void thereAreNoLetters(int count){
    number = "no";
    verb="are";
    pluralModifier = "s";
  }
  
  
}
```



### Don't Add Gratuitous Context - 불필요한 맥락을 없애라

* Gas Station Deluxe 라는 어플리케이션을 짠다고 가정 모든 클래스 이름을 GSD로 시작하는건 ... 

* 일반적으로 짧은 이름이 긴 이름보다 좋다. 단 의미가 분명한 경우에 한해서

* 이름에 불필요한 맥락을 추가하지 않도록 주의한다.

* accountAddress / customerAddress는 Address 클래스 인스턴스로는 좋은 이름이지만 클래스 이름으로는 좋지 않다.

* Address는 클래스 이름으로 적합하다. 
  * 포트주소, mac주소, 웹주소를 구분해야하면 PostalAddress, Mac, URI도 갠춘함



## Final Words

좋은 이름을 선택하려면, 설명 능력이 뛰어나야 하고, 문화적 배경이 같아야한다.

뭐 어렵지만 잘 바꿔보려고 하자인듯 남이 질책할지 모른다고 고민하지말고.













### 
















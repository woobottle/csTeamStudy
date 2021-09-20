# 객체지향 개발 5대 원리: SOLID

* Single Responsibility Principle(단일 책임의 원칙)
* Open Close Principle(개방폐쇄의 원칙)
* Liskov Substitution Principle(리스코브 치환의 원칙)
* Interface Segregation Principle(인터페이스 분리의 법칙)
* Dependency Inversion Principle(의존성역전의 원칙)


### Single Responsibility Principle(단일 책임의 원칙)

i. 정의 : 클래스는 하나의 기능만을 수행해야 한다. 
        클래스가 제공하는 모든 서비스는 그 하나의 책임을 수행하는데 집중되어 있어야 한다. => 어떤 변화에 의해 클래스를 변경하여야 하는 이유는 하나뿐이어야 한다.

ii. 적용방법 : 클래스당 단 하나의 책임만을 맡도록 한다. 
           두 클래스간의 관계의 복잡도를 줄이도록 설계.
           책임을 기존의 어떤 클래스로 모으거나, 새로운 클래스를 만들어 해결 => 응집성을 높이는 방향으로 
           응집성은 높게 의존성은 낮게

iii. 적용사례
```java
  // 적용 전
  class Guitar(String serialNumber, double price, Maker maker, Type type, String model, Wood backWood, Wood topWood, int stringNum) { 
    // serialNumber 빼고는 모두 변경이 발생 할 수 있는 부분, 즉 변화요소 
    // 변화요소가 바뀌게 된다면 코드를 전부 변경해줘야 한다.
    // 따라서 따로 뺀다
    this.serialNumber = serialNumber;
    this.price = price;
    this.maker = maker;
    this.type = type;
    this.model = model;
    this.backWood = backWood;
    this.topWood = topWood;
    this.stringNum = stringNum;
  }

  private String serialNumber;
  private double price;
  private Maker maker;
  private Type type;
  private String model;
  private Wood topWood;
  private Wood backWood;
  private int stringNum;


  // 적용 후
  class Guitar() {
    public Guitar(String serialNumber, GuitarSpec spec) {
      this.serialNumber = serialNumber;
      this.spec = spec;
    }

    private String serialNumber;
    private GuitarSpec spec;
  }

  class GuitarSpec() {
    double price;
    Maker maker;
    Type type;
    String model;
  }
```

### Open Close Principle(개방폐쇄의 원칙)
i. 정의 : 구성요소(컴포넌트, 클래스, 모듈, 함수)의 확장에는 열려있고, 변경에는 닫혀 있어야 한다.
         요구사항의 변경이나 추가사항이 발생하더라도 기존 구성요소는 수정이 일어나지 말아야 하고, 기존 구성요소를 사용해 확장할 수 있어야 한다.

ii. 적용방법 : (인터페이스의 활용)
         1. 변경될 것과 변하지 않을 것을 엄격히 구분합니다
         2. 두 모듈이 만나는 지점에 인터페이스를 정의 합니다.
         3. 구현에 의존하기 보다 정의한 인터페이스에 의존하도록 코드를 작성 합니다.

iii. 적용사례
```java
  // 적용 전
  class Guitar() {
    public Guitar(String serialNumber, GuitarSpec spec) {
      this.serialNumber = serialNumber;
      this.spec = spec;
    }
    private GuitarSpec spec;
  }

  class GuitarSpec() {}

  class Violin() {
    public Violin(String serialNumber, ViolinSpec spec) {
      this.serialNumber = serialNumber;
      this.spec = spec;
    }
    private ViolinSpec spec;
  }

  class ViolinSpec() {}


  // 적용 후
  class Guitar extends StringInstrument() {
    public Guitar(String serialNumber, GuitarSpec spec) {
      this.serialNumber = serialNumber;
      this.spec = spec;
    }
    private GuitarSpec spec;
  }

  class GuitarSpec extends StringInstrumentSpec() {}

  class Violin extends StringInstrument() {
    public Violin(String serialNumber, ViolinSpec spec) {
      this.serialNumber = serialNumber;
      this.spec = spec;
    }
    private ViolinSpec spec;
  }

  class ViolinSpec extends StringInstrumentSpec() {}
```

iv. 적용이슈
  인터페이스는 가능하면 변경되어서는 안 됩니다. 여러 경우의 수에 대한 고려와 예측이 필요합니다.
### Liskov Substitution Principle(리스코브 치환의 원칙)

i. 정의 : 서브 타입은 언제나 기반 타입으로 교체할 수 있어야 한다. 
         서브 클래스가 확장에 대한 인터페이스를 준수해야 한다.
         (뭔소린지 잘 모르겠다. 예시를 살펴봐야겠다)

ii. 적용방법 :
        1. 만약 두 개체가 똑같은 일을 한다면 둘을 하나의 클래스로 표현하고 이들을 구분할 수 있는 필드를 둡니다.(enum 개념인가)
        2. 똑같은 연산을 제공하지만, 이들을 약간씩 다르게 한다면 공통의 인터페이스를 만들고 둘이 이를 구현 합니다.(인터페이스 상속)
        3. 공통된 연산이 없다면 별개의 클래스를 만듭니다
        4. 두 개체가 하는 일에 추가적으로 무언가를 더 한다면 구현 상속을 사용합니다.

iii. 적용사례 :
```java
  // 적용 전
  // LinkedList가 아니라 hashSet을 써야한다면 이 쪽 코드는 변경이 되어야 한다. 
  // 이러한 작업이 자료구조가 바뀔때마다 생길 듯
  void f() {
    LinkedList list = new LinkedList();
    modify(list);
  }

  void modify(LinkedList list) {
    list.add();
    doSomethingWith(list);
  }

  // 적용 후
  void f() {
    Collection collection = new HashSet();
    modify(collection);
  }

  void modify(Collection collection) {
    collection.add();
    doSomethingWith(collection);
  }
  // LinkedList와 HashSet 모두 Collection 인터페이스를 상속하고 있으므로 위와 같이 작성하는 것이 좋다.
  // Collection 생성 부분만 고치면 Collection 구현 클래스를 사용할 수 있다.
  // Collection 이 지원하지 않는 연산을 사용한다면 한 단계 계층 구조를 내려가야 한다.
  // ArrayList, LinkedList, Vector을 사용해야 한다면 이들이 구현하고 있는 List를 사용하는 것이 현명하다
```

### Interface Segregation Principle(인터페이스 분리의 원칙)

i. 정의 : 한 클래스는 자신이 사용하지 않는 인터페이스는 구현하지 말아야 한다.
         어떤 클래스가 다른 클래스에 종속될 때는 가능한 최소한의 인터페이스만을 사용해야 한다.
         인터페이스의 단일 책임을 강조

ii. 적용방법 :
        1. 클래스 인터페이스를 통한 분리
        2. 객체 인터페이스를 통한 분리


iii. 적용사례 
```java
  // JTable 클래스에는 굉장히 많은 메소드들이 있고 여러 인터페이스 들을 제공하고 있다.
  // Accessible, CellEditorListenr, ListSelectionListener, Scrollable, TableColumnModelListener, TableModleListener 등이 있는데 
  // 이중 필요한 인터페이스만 가져와서 사용한다.
  import javax.swing.event.*;
  import javax.swing.table.TableModel;

  public class SimpleTableDemo implements TableModelListener {
    public SimpleTableDemo() {
      table.getModel().addTableModelListener(this);
    }

    // 인터페이스를 통해 노출할 기능을 구현합니다.
    public void tableChanged(TableModelEvent e) {
      int row = e.getFirstRow();
      int column = e.getColumn();
      TableMdel model = (TableModel)e.getSource();
      String columnName = model.getColumnName(column);
      Object data = model.getValueAt(row, column);
      // Do Something with the data
    }
  }
```
### Dependency Inversion Principle(의존성역전의 원칙)

i. 정의 : 하위 레벨 모듈의 변경이 상위 레벨 모듈의 변경을 요구하는 위계관계를 끊는 의미의 역전, 관계를 최대한 느슨하게 만드는 원칙


출처 : https://www.nextree.co.kr/p6960/
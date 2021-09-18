책의 5장에서 

서로 밀접한 개념은 세로로 가까이 둬야 한다. 
물론 두 개념이 서로 다른 파일에 속한다면 규칙이 통하지 않는다.
하지만 타당한 근거가 없다면 서로 밀접한 개념은 한 파일에 속해야 마땅하다.
이게 바로 protected 변수를 피해야 하는 이유 중 하나다.

라고 하였다.
protected 변수를 피해야 하는 이유는 
protected 변수로 선언하였을 경우 다른 패키지에서도 참고할 수 있게 되므로 개념을 분리한 이유가 약해진다고 이해하였다.
(기껏 패키지로 분리했는데 다른 패키지에서 상속받아서 접근 가능하면 의존성이 증가되는것 같다.)

자바에는 

1. public
어떤 클래스에서라도 접근 가능
```java
package jump2java.house;

public class HousePark {
  protected String lastname = "park";
  public String info = "this is public message";
}
```

1. default
```java
package jump2java.house;

public class HouseKim {
  String lastname = "kim";
}

package jump2java.house;

public class HousePark {
  String lastname = "park";

  public static void main(String[] args) {
    HouseKim kim = new HouseKim();
    System.out,println(kim.lastname);
  }
}

// 접근 제어자 선언이 없을경우 default로 선언되며
// 해당 패키지 내에서만 접근이 가능하다.
```

3. protected

동일 패키지내의 클래스 또는 해당 클래스를 상속받은 외부 패키지의 클래스에서 접근이 가능하다
```java
package jump2java.house;

public class HousePark {
  protected String lastname = "park";
}

package jump2java.house;

import house.HousePark;

public class EungYongPark extends HousePark {
  public static void main(String[] args) {
    EungYongPark eyp = new EungYongark();
    System.out.println(eyp.lastname);
  }
}

// HousePark를 상속받은 EungYongPark은 HousePark과 패키지 이름이 다르지만 
// lastname이 protected로 선언되었으므로 eyp.lastname으로 접근이 가능하다.
// HousePark의 lastname이 default 였다면 컴파일 에러 발생
```

4. private
```java
  public class AccessModifier {
    private String secret;
    private String getSecret() {
      return this.secret;
    }
  }
  // AccessModifier 클래스에서만 접근이 가능하다 
```

public은 패키지 상관없이 모든 클래스에 접근 가능
default는 동일 패키지 일때만 접근 가능
protected는 다른 패키지 일경우 상속을 받거나 동일 패키지인 경우
private은 자기자신 클래스 내에서만 접근 가능




출처 : https://wikidocs.net/232
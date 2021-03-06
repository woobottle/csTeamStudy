# 배열
- 인덱스만 알고 있으면 O(1). 값만 알고 있으면 최악의 경우 O(n).
- 연결리스트에 비해 룩업 연산은 빠르지만 배열 중간 데이터의 삭제, 추가는 느려짐. 배열의 데이터를 물리적으로 옮겨 새로운 배열을 만들어야하기 때문. - O(n)
- 유한하고 고정된 수의 원소로 이루어짐.
- 저장해야할 원소의 개수를 미리 알고 있는 경우 배열 사용.
- 최신의 언어들은 대부분 동적 배열 지원. 
  - 동적 배열 구현에서도 내부적으로는 정적 배열 사용.
  - 크기를 바꿀 때 적당한 크기의 배열을 새로 만들어 모든 원소를 복사하고 기존 메모리를 해제.
  - 이 연산은 꽤 느리기에 최대한 자제해야 함.

<br/>

## C/C++
- 포인터 상수란? 
  - ```char *const chrPtr``` 같은 식으로 선언.
  - 메모리상의 다른 위치를 가리키도록 변경할 수는 없지만 그 포인터가 가리키는 메모리에 있는 내용을 바꾸는데 사용.
- 단순하게 대입만 해서는 한 배열의 원소들을 다른 배열의 원소들로 초기화 할 수 없음.
- ex) ```arrayA = arrayB``` 와 같이 사용할 수 없음.
- 반복문을 써서 한 원소씩 대입하거나 memcpy 같은 라이브러리 사용해야함.

<br/>

## 자바
- 배열에 대한 레퍼런스와 배열 원소에 대한 레퍼런스가 같지 않음.
- 두 배열 레퍼런스의 유형이 같으면 한 레퍼런스를 다른 레퍼런스에 대입하는 것이 가능.
```java
// 두 변수가 모두 같은 배열을 참조하게 됨.
byye[] arrayA = new byte[10];
byye[] arrayB = new byte[10];
arrayA = arrayB
```
- 한 배열을 다른 배열로 복사하고 싶으면 loop를 돌리거나 시스템 함수 호출해야 함.
```java
if (arrayB.length <= arrayA.length) {
  System.arraycopy( arrayB, 0, arrayA, 0, arrayB.length )
}
```

<br/>

## C#
- 자바와 같이 ```foo[2][3]``` 같은 문법도 지원하고 ``` foo[2, 3]``` 같은 다차원 배열 문법도 지원함.
- 자바 : 다차원 배열에서 배열 원소로 들어가는 배열의 길이가 서로 다를 수 있어 불규칙적이기 때문에 불규칙 배열이라고 함.(행렬이 직사각형 형태가 아닌 삼각형 등등)

<br/>

## js
- js에서 배열은 Array 객체의 인스턴스.
- 자동으로 크기가 조절.

<br/>

# 문자열
- [유니코드의 멀티바이트 인코딩](https://onlywis.tistory.com/2)
- 최근에 설계된 언어는 여러 바이트로 이루어진 기본 문자 유형이 존재. 하지만 c, c++의 char는 무조건 한 바이트임.
- 자바와 C#에서는 UTF-16 인코딩을 사용.
  - 유니코드의 대부분을 하나의 16비트 char로 표현, 나머지는 두개의 char로 표현.
- 네트워크를 통해 전송되는 텍스트나 파일에 저장된 텍스트 용도로 UTF-8 인코딩을 사용.
  - 최대 네개의 바이트를 사용하여 모든 유니코드의 코드 포인트를 인코딩.
  - 모든 ASCII 문자열을 한 바이트로 표현할 수 있음.
- [가변결이 인코딩](https://hyoje420.tistory.com/3)
  - 문자열을 저장하기 위해 쓰인 char 개수보다 문자열에 들어가는 문자 개수가 적을 수 있음.
  - 여러개의 char로 인코딩한 한 코드 포인트를 구성하는 글자 중 하나를 완전한 문자로 처리하는 일이 없어야 할 것.
- 어떤 인코딩을 사용하든 문자열을 내부적으로는 배열을 써서 표현.

<br/>

## C
- C의 문자열은 char 배열에 저장.
- 문자열의 끝은 '\0'으로 표현되는 NUL 문자로 표시(값이 0인 char 유형 NUL은 메모리 주소 0을 가리키는 NULL과 다름)
- 문자 배열에는 종결자가 들어갈 공간이 있어야함.
  - 10개의 문자열의 경우 11개의 문자가 들어갈 수 있는 배열이 필요.
  - 이러한 문자열의 표현 방식 때문에 문자열의 길이를 구하는 연산은 O(n) 연산이 됨.
  - 문자열의 길이를 반환하는 strlen() 함수에서 문자열의 끝이 나올 때 까지 반복 수행.
- 서로 다른 배열을 한쪽에 대입할 수 없는 것 처럼 문자열도 = 연산자를 통해 복사할 수 없음. ```strlcpy()```를 사용해야함.
- 문자열의 길이를 변경할 떄는 새로운 마지막 글자 뒤에 널 문자를 반드시 삽입해야함.
  - 문자 배열에 새로운 문자열과 종결 문자가 모두 들어갈 수 있는지도 확인해야 함.

<br/>

## C++
- C++ 문자열은 NUL 문자로 종결되지 않기 때문에 널 바이트도 저장할 수 있음.
- 문자열의 사본을 만들면 가능한 하나의 [버퍼](https://dololak.tistory.com/84)를 공유하지만 문자열은 변형 가능하기 때문에(mutable)(문자열이 바뀔 수 있기 때문에) 필요한 경우 새로운 버퍼가 만들어진다.

<br/>

## 자바
- 자바의 문자열은 String이라는 시스템 클래스의 객체.
- 문자열을 문자 및 바이트 배열과 상호 변환 가능.
- 문자열에 있는 개별 문자는 직접 액세스할 수 없고 String 클래스에 있는 메서드를 써야만 액세스 가능.
- C++과 마찬가지로 가능한 경우에는 같은 문자열끼리는 같은 배열 공유.
- 자바의 문자열은 변형 불가능(unmutable)함. 일단 문자열이 생성되고 나면 바꿀 수가 없다. 문자열을 조작하는 메서드도 사실은 새로운 문자열 인스턴스를 반환함.
- "+" 연산자를 사용하여 두 개의 String 인스턴스를 연결하면 컴파일러는 내부적으로 StringBuilder 인스턴스를 사용함. 이 + 연산자는 편리하긴 하지만 비효율적인 코드를 만들어낼 가능성이 존재함(반복문)
```java
String s = "";
for ( int i = 0; i < 10; ++i ) {
  s = s + i + " ";
}

// 위 코드는 아래와 같음.

String s = "";
for ( int i = 0; i < 10; ++i ) {
  StringBuilder t = new StringBuilder();
  t.append( s );
  t.append( i );
  t.append( " " );
  s = t.toString();
}
```

- 위 코드를 아래와 같이 바꾸면 더 효율적임.
```java
StringBuilder b = new StringBuilder();
for ( int i = 0; i < 10; ++i ) {
  b.append( i );
  b.append( " " );
}
String s = b.toString();
```

<br/>

# 배열과 문자열 문제

## 반복되지 않은 첫 번째 문자 찾기
> 문자열에서 처음으로 반복되지 않은 문자를 효율적으로 찾아내는 함수 작성. ex) total -> o / teeter -> r
- 각 문자를 나머지 문자와 비교할 경우 O(n^2)
- 이진트리 - O(log(n))
- 배열 && 해시테이블 - O(1)

### 배열과 해시테이블 사용
- 배열 또는 해시테이블을 쭉 훑으면서 값이 1인 문자를 찾는다.
- 원래 문자열에 있는 문자 순서대로 값을 검색한다. 1이 나오면 return.
- 최악의 경우 문자열에 있는 모든 문자들에 대해 두 번씩의 연산만 하면 됨. O(n)
- 배열과 해시테이블의 가장 큰 차이점은 메모리 요구량. 
  - 배열은 가능한 모든 문자 개수만큼의 원소가 필요.
  - 해시테이블은 입력된 문자열에 들어 있는 서로 다른 문자 개수만큼 저장할 공간만 있으면 됨.
  - 문자의 개수가 적으면서 긴 문자열을 처리할 때는 배열.
  - 문자열이 짧은 경우나 문자 개수가 많은 인코딩을 사용하는 경우는 해시테이블.

``` C#
  public static Character firstNonRepeated( String str ) {
    HashMap<Character, Integer> charHash = new HashMap<Character, Integer>();

    int i, length;
    Character c;

    length = str.length;

    for (i=0; i < length; i++) {
      c = str.charAt(i);
      if (charHash.containsKey(c)) {
        charHash.put(c, charHash.get(c) + 1);
      } else {
        charHash.put(c, 1);
      }
    }

    for (i = 0; i < length; i++) {
      c = str.charAt(i);
      if (charHash.get(c) == 1) return c;
    }

    return null;
  }
```
- 자바의 경우.
  - 자바 컬렉션 클래스는 레퍼런스 유형에 대해서만 쓸 수 있음.
  - 어떤 키와 연관된 값을 증가시킬 때마다 이전 값을 저장하고 있던 Integer 객체는 버리고 증가된 값이 저장된 Integer 객체를 새로 만들어야 함.
  - 문자가 0번, 1번, 두번 이상 3가지 케이스로 나눈다.
  - 해시테이블의 경우는 한번, 두번 이상을 표시하기 위한 Object 값 두개만 만들고 해시 테이블에 그 객체를 저장하는 방법을 쓰면 된다.

```java
  public static String firstNonRepeated( String str ){
    HashMap<Integer, Object> charHash = new HashMap<Integer, Object>();
    Object seenOnce = new Object(), seenMultiple = newObject();
    Object seen;
    int i;
    final int length = str.length;

    for (i=0; i < length;){
      final int cp = str.codePointAt(i);
      // 왜 charCount?
      i += Character.charCount(cp);
      seen = charHash.get(cp);
      if (seen == null) {
        charHash.put(cp, seenOnce);
      } else {
        if (seen == seenOnce) {
          charHash.put(cp, seenMultiple);
        }
      }
    }

    for (i=0; i < length) {
      final int cp = str.codePointAt(i);
      i += Character.charCount(cp);
      if (charHash.get(cp) == seenOnce) {
        return new String(Character.toChars(cp));
      }
    }
    return null;
  }
```
- ### ***charCount***
  - Character 클래스의 [charCount method](https://www.javatpoint.com/post/java-character-charcount-method)를 왜 사용하는가
  - 지정된 문자 (Unicode 코드 포인트)를 나타내는데 필요한 char값의 수를 판단
  - charCount는 매개변수가 0X10000보다 크면 2 작으면 1을 리턴.
  - String의 length는 unicode code unit의 숫자를 리턴함.
  ```java
  String 🂡 length : 2  
  String A length : 1
  ```
  - java에서는 기본적으로 16비트 문자열만 지원하다가 Supplementary Characters를 도입하여 32비트로 유니코드를 표현한다. 즉, 기본적인 16비트에 해당하는 문자같은 경우 2바이트의 0XFFFF보다 작기 때문에 length가 1로 나오고 Supplementary Characters가 필요한 문자같은 경우 2로 나오게 되는 것.
    - Basic Multilingual Plane 문자는 2byte로 표현하고,
    - Supplementary Characters 문자는 두개의 Unicode code unit(HighSurrogate + LowSurrogete)를 이용하여 4byte로 표현한다.
    - 16비트라하면 2^16 만큼의 문자열을 포함. 32비트는 2^32 만큼의 문자열을 포함.
  - https://hianna.tistory.com/95?category=650599
  - https://hianna.tistory.com/96
  - python :  <img src="https://user-images.githubusercontent.com/72545106/139770140-fcbfdad3-9ca3-4b5f-b12e-6c5e0ae1f42f.png"  alt="python" width="200" />
  - js :  <img src="https://user-images.githubusercontent.com/72545106/139770144-98a53bbd-7995-4a4a-859a-c13082ffc777.png"  alt="js" width="200" />
  - ruby : <img src="https://user-images.githubusercontent.com/72545106/139770146-a3b95f62-b334-40ff-be7b-32487d5c854b.png"  alt="ruby" width="200" />




<br/>

## 특정문자 제거
> 변형 가능한 ASCII 문자열에서 문자를 삭제하는 함수 작성. str과 remove 두 인자를 받아들임. remove에 있는 모든 문자를 str에서 제거해야 함.  
>
> ex) "Battle of Vowels: Hawaii vs. Grozny" 에서 aeiou가 remove 인자로 주어지면 "Bttl f Vwls: Hw vs. Grzny"로 변환해야함.


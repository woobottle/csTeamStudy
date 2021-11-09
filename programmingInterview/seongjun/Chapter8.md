# 재귀 호출

* 자기 자신을 호출하는 루틴

## 이해

* recursion은 유사한 하위 작업 형태로 정의할 수 있는 작업을 처리하는 데 유용하게 쓰임
* 정렬이나 검색, 종주 문제에는 간단한 재귀적인 형태의 풀이가 있는 경우가 흔함
* 재귀호출하다보면 자신을 호출하지 않고도 처리할 수 있는 하위 작업이 나온다. - 이를 base case라고함
* 자신을 호출해서 하위를 해결하는게 recursive case
* 반환한 값 그 자체가 곧바로 반환되면 꼬리 재귀 호출이라고 함 - tail recursive
  * factorial은 반환된 값을 바로 반환하지 않고 곱셈하고 반환하니까 아님
* 일부 컴파일러에서는 꼬리 재귀 호출 함수에 대해 꼬리 호출 제거 tail call elimination 을 함
  * 각 호출에 대해 같은 스택 프레임을 재사용하는 최적화 적용
* 재귀 호출 레벨을 추적하기 위한 인자 또는 추가 자료구조가 필요함
* n! 외에 중간 결과까지 반환하는 루틴? 정수 배열을 할당..
  * 래퍼함수를 써서 처리하는 것이 제일 쉽다.

```c++
int[] allFactorials( int n ){
  int[] results = new int[ n==0 ? 1 : n ];
  doAllFactorials( n, results, 0 );
  return results;
}
int doAllFactorials( int n, int[] results, int level ){
  if ( n > 1){
    results[level] = n * doAllFactorials ( n-1, results, level + 1);
    return results[level];
  }else{
    results[level] = 1;
    return 1;
  }
}
```

* 강력한 테크닉이긴 하지만 가장 좋은 접근법이라고는 못함
* 가장 효율적인 접근법인 경우는 거의 없음
* 계산보다는 호출에 따르는 오버헤드가 더 많은 시간을 소모함
* 반복적인 구현법으로도 가능은 함
* 반복적인 구현법이 잘 안떠오르면...
* 결국 재귀도 스택, 직접 스택 만들고 수동으로 넣고 꺼내쓰면..
* 대신 스택으로 루틴 만들기는 재귀볻 ㅏ어려울 수 있음
* 많이 빠르지도 않음 사실

## 이진 검색

> 정렬된 정수 배열에 대해 이진 검색을 수행하여 주어진 정수의 인덱스를 찾아내는 함수를 구현하라
>
> 이 검색 방법의 효율을 따져보고 다른 검색 방법과 비교해보라

이미 정렬된거에서 하는거 알죠?

* 어떤 오류를 처리해야 하는지 생각, 어떤 가정을 하는지
* 찾아낸다고 가정하고 하면 안댐! 예외

```java
if( range < 0 ){
  throw new BSException('~')
}
if( array[lower] > array[upper] ){
  throw new BSException("Array Not Sorted")
}
```

```java
while(true){
  range = upper - lower;
...
  cetner = (range/2)+lower;
  if(target == array[center]){
    return center;
  }else if(target < array[center]){
    upper = center -1;
  }else{
    lower = center + 1;
  }
}
```

## 문자열 순열

> 어떤 문자열에 있는 문자들을 나열하는 모든 가능한 순서를 출력하는 루팅을 구현하라
>
> 원본 문자열에 있는 모든 문자들을 사용하는 모든 순열을 출력하면ㄷ ㅚㄴ다.

* 들어갈 문자를 고르고, 선택한 문자를 바꾸기 전에 다음 위치부터 시작해서 오른쪽으로 가면서 반복

```markdown
* 마지막 위치를 지나갔으면
  * 문자열 출력
  * 반환
* 그렇지 않으면
  * 입력한 문자열에 있는 각 글자에 대해
  * 사용한 것으로 표시되어 있으면 다음 글자로 넘어감
  * 그렇지 않으면 그 글자를 현재 위치에 집어넣음
    * 그 글자를 사용한 것으로 표시
    * 현재 위치 + 1 위치에서 시작하여 나머지 글자들을 나열
    * 그 글자를 사용하지 않은 것으로 표시
```

* 재귀호출 케이스와 기본 케이스를 분리하는 것은 좋음
* 다음 재귀 호출에서 기본 케이스를 호출하게 되면 재귀호출을 하지 않고 기본 케이스를 바로 호출하면? 최적화
* 흠..... 


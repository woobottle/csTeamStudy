# 9. 정렬

정렬 알고리즘을 직접 구현할 일은 거의 없겠지만 각각의 차이와 장단점에 대해서는 알아둘 필요가 있다.

### 정렬 알고리즘
고려해야할 사항들
* 정렬할 데이터의 양
* 데이터와 메모리 => 대부분 정렬 알고리즘은 처리할 데이터가 메모리에 있을 때만 효율적으로 돌아간다.
* 데이터가 정렬된 정도
* 필요한 추가 메모리의 양
* 상대 위치 보존 여부

##### 선택정렬
=> 배열 순회하면서 가장 작은 값 찾고 이걸 첫번째 인덱스에, 다시 순회하면서 첫번째 인덱스 제외한 곳에서 찾은 제일 작은 값을 두번째 인덱스에

```java
// 재귀적인 선택 정렬로 배열을 정렬
public static void selectionSortRecursive(int[] data) {
  selectionSortRecursive(data, 0);
}

// 주어진 인덱스에서 시작하는 부분 배열을 정렬
private static void selectionSortRecursive(int[] data, int start){ 
  if (start < data.length - 1) {
    swap(data, start, findMinimumIndex(data, start));
    selectionSortRecursive(data, start + 1);
  }
}

private static int findMinimumIndex(int[] data, int start) {
  int minPos = start;

  for (int i = start + 1; i < data.length; ++i) {
    if (data[i] < data[minPos]) {
      minPos = i;
    }
  }
  return minPos;
}

private static void swap(int[] data, int index1, int index2) {
  if (index1 != index2) {
    int tmp = data[index1];
    data[index1] = data[index2];
    data[index2] = tmp;
  }
}
```
선택 정렬의 장점은 원소를 맞바꾸는 횟수가 최대 n-1 번이라는 점이다.

##### 삽입 정렬
=> 한 번에 한 원소씩 이미 정렬된 다른 원소들과 비교하여 새 원소를 제 위치에 삽입하는 식으로 정렬된 배열을 만든다.

```java
public static void insertionSort(int[] data) {
  for (int which = 1; which < data.length; ++which) {
    int val = data[which];
    for (int i = which - 1; i>= 0; --i) {
      if (data[i] > val) {
        data[i+1] = data[i];
        data[i] = val;
      } else {
        Break;
      }
    }
  }
}
```

##### 퀵 정렬
한 피벗 값을 기준으로 작은 값은 왼쪽으로 큰 값은 오른쪽으로 보내버린다

```java
public static void quicksortSimple(int[] data) {
  if (data.length < 2) {
    return;
  }

  int pivotIndex = data.length / 2;
  int pivotValue = data[pivotIndex];

  int leftCount = 0;

  // 피벗보다 작은 원소 개수 세기
  for (int i = 0; i < data.length; ++i) {
    if (data[i] < pivotValue) ++leftCount;
  }

  int[] left = new int[leftCount];
  int[] right = new int[data.length - leftCount - 1];
  int l = 0;
  int r = 0;

  for (int i = 0; i< data.length; ++i) {
    if ( i == pivotIndex) continue;

    int val = data[i];

    if (val < pivotValue) {
      left[l++] = val;
    } else {
      right[r++] = val;
    }
  }

  quickSortSimple(left);
  quickSortSimple(right);

  System.arraycopy(left, 0, data, 0, left.length);
  data[left.length] = pivotValue;
  System.arraycopy(right, 0, data, left.lenfth + 1, right.length);
}
```

##### 머지 소트
logN의 시간복잡도를 가지는 머지 소트

```java
public static void mergeSortSimple(int[] data) {
  if (data.length < 2) {
    return;
  }

  int mid = data.length / 2;
  int[] left = new int[mid];
  int[] right = new int[data.length - mid];

  System.arraycopy(data, 0, left, 0, left.length)
  System.arraycopy(data, mid, right, 0, right.length)

  mergeSortSimple(left);
  mergeSortSimple(right);
  merge(data, left, right)
}

public static void merge(int[] dest, int[] left, int[] right) {
  int dind = 0;
  int lind = 0;
  int rind = 0;

  while (lind < left.lenfth && rind < right.length) {
    if (left[lind] <= right[rind])  {
      dest[dind++] = left[lind++];
    } else {
      dest[dind++] = right[rind++];
    }
  }

  while(lind < left.lenfth) 
    dest[dind++] = left[lind++]
  while(rind < right.length) 
    dest[dind++] = right[rind++]
}
```

### 정렬 문제
1. 안정적인 선택 정렬 
> 안정적인 버전의 선택 정렬을 구현하라

```java
public static void selectionSort(int[] data) {
  for (int start = 0; start < data.length - 1; ++start) {
    swap(data, start, findMinimumIndex(data, start));
  }
}
```
이게 왜 불안정한거지???

**안정적인 정렬 알고리즘 => 키가 같은 원소의 순서를 입력된 순서 그대로 유지시켜주는 정렬 알고리즘**

위의 코드가 불안정한 이유 => [5(1), 3, 5(2), 2] 가 정렬되면 [2, 3, 5(1), 5(2)] 혹은 [2, 3, 5(2), 5(1)] 이런 식으로 나와버릴 수가 있다.

키가 같은 원소의 순서가 정렬 때마다 바뀔수가 있다.

그래서 **배열을 옆으로 밀어내는 방식**으로 작업해야 한다.

```java
public static void selectionSortStable(int[] data) {
  for (int start = 0; start < data.length -1; ++start) {
    insert(data, start, findMinumumIndex(data, start));
  }
}

// 배열을 옆으로 밀어내는 방식으로 데이터를 삽입
private static void insert(int[] data, int start, int minIndex) {
  if (minIndex > start) {
    int tmp = data[minIndex];
    System.arraycopy(data, start, data, start + 1, minIndex - start);
    data[start] = tmp;
  }
}
```

2. 다중 키 정렬 
> 직원에 대한 정보를 저장하기 위한 다음과 같은 객체로 이루어진 배열이 있다.   
> public class Employee {   
>   public String extension;    
>   public String givenname;    
>   public String surname;   
> }    
> 표준 라이브러리의 정렬 루틴을 이용하여 회사 전화번호부처럼 성 알파벳순, 그리고 이름 알파벳순으로 정렬하라

```java
import java.util.Comparator;

public class EmployeeNameComparator implements Comparator<Employee> {
  public int compare(Employee e1, Employee e2) {
    int ret = e1.surname.compareToIgnoreCase(e2.surname);

    if (ret == 0) {
      ret = e1.givenName.compareToIngoreCase(e2.givenname);
    }
    return ret;
  }
}

public static void sortEmployees(Employee[] employees) {
  Arrays.sort(employees, new EmployeeNameComparator());
}
```

python에서는 sort의 key 파라미터를 이용할것 같다.

3. 최적화된 퀵 정렬

> 효율적인 제자리 버전의 퀵 정렬 알고리즘을 구현하라.

=> 메모리의 재할당을 막기 위해 swap하는 방식으로 구현을 하는게 좋다.

퀵 정렬을 구현하는 가장 간단한 방법은 L(작은 애들)과 G(큰 애들)용으로 새 목록을 할당하고 재귀 호출에서 리턴되고 나면 거기서 다시 결과를 복사해오는 방식 => 효율도 좋지 않고 추가 메모리도 있어야 한다.

메모리 할당 문제는 파티션을 나누는 단계, 즉 값을 L과 G로 재배치하는 단계에서 발생한다. 파티션 작업을 생각해보면 원소 수에는 변함이 없고 위치만 바뀔 뿐이기 때문에 L, 피벗, G를 모두 원래 배열에 저장할 수 있어야 한다.

```
피벗 값 선택
첫 번째 원소를 현재 위치로 하여 시작
G의 head 위치를 배열의 마지막 원소로 지정
현재 위치 < G의 head 위치가 만족되는 동안
  현재 원소가 피벗보다 작으면 
    현재 원소를 앞으로 전진
  그렇지 않으면
    현재 원소를 G의 head와 맞바꾸고 G의 헤드를 앞으로 전진
배열의 L과 G 부분에 대해서 이 루틴 재귀 호출
```

배열에 있는 모든값이 같으면 재귀호출이 끝나지가 않는다.

```java
public static void quicksortOptimized(int[] data) {
  quicksortOptimized(data, 0, data.length - 1);
}

public static void quicksortOptimized(int[] data, int left, int right) {
  int pivotValue = data[(int)((((long)left) + right) /2)];
  int i = left;
  int j = right;

  // 값을 바꿔주기만 할뿐 새로운 변수의 생성이나 이러한 것은 없다.
  // 가장 메모리가 비효율적으로 쓰이는 곳이 배열 변수의 재생성 이기 때문
  while (i <= j) {
    while (data[i] < pivotValue) i++;
    while (data[j] > pivotValue) j--;
    if (i <= j) {
      swap(data, i, j);
      i++;
      j--;
    }
  }

  if (left < j) {
    quicksortOptimized(data, left, j);
  }
  if (i < right) {
    quicksortOptimized(data, i, right);
  }
}
```
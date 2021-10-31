## 트리
- 0개 이상의 다른 노드에 대한 레퍼런스(또는 포인터)가 들어 있는 노드로 구성.  
- 연결리스트와 마찬가지로 구조체나 클래스로 표현
- 객체지향 언어에서는 노드의 공통적인 부분을 하나의 클래스로 정의. 노드에 들어가는 데이터를 위해 서브클래스 정의.
``` java
// java
public abstract class Node {
  // 이 노드에서 참조하는 모든 노드를 children 배열에 담음.

  private Node[] children;

  public Node( Node[] children ) {
    this.children = children;
  }
  
  public int getNumChildren() {
    return children.length;
  }

  public Node getChild( int index ) {
    return children[ index ];
  }
}

// 노드에 들어가는 데이터를 위해 서브클래스 정의.
public class IntNode extends Node {
  public int value;

  public IntNode( Node[] children, int value ) {
    super( children );
    this.value = value;
  }

  public int getValue() {
    return value;
  }
}
```
- 최상위 노드를 루트 노드(root)

<br/>

## 이진트리
- 한 노드에 자식이 최대 두 개까지만 존재. 왼쪽 자식, 오른쪽 자식.

```c#
public class Node {
  private Node left;
  private Node right;
  private int value;

  public Node (Node left, Node right, int value) {
    this.left = left;
    this.right = right;
    this.value = value;
  }

  public Node getLeft() { return left; }
  public Node getRight() { return right; }
  public Node getValue() { return value; }
}
```
<br/>

## 이진 검색 트리(Binary Search Tree)
- 노드의 왼쪽 자식의 값은 항상 자신의 값 이하. 오른쪽 자식은 항상 자신의 값 이상.
- 룩업 연산(Lookup)(트리에 있는 특정 노드의 위치를 알아내는 연산)을 빠르고 간단하게 처리할 수 있음.

```C#
Node findNode( Node root, int value ) {
  // 현재 노드가 널이 아닌 동안 반복
  while ( root != null ) {
    // 루트 노드에서 시작
    int currval = root.getValue();
    // 현재 노드의 값이 찾고자 하는 값이면 현재 노드 리턴.
    if ( currval == value ) break;
    // 현재 노드의 값이 찾고자 하는 값보다 작으면 오른쪽 리턴
    if ( currval < value ) {
      root = root.getRight();
    // 현재 노드의 값이 찾고자 하는 값보다 크면 왼쪽 리턴
    } else { // currval > value
      root = root.getLeft();
    }
  }

  return root;
}
```
- 이진검색 트리는 최악의 경우 각 노드마다 자식이 하나씩 밖에 없을 수 있으므로 O(n)이고 최상의 경우 각 노드마다 자식이 둘이 있을경우 O(log(n)) 이다.
- 한 노드에서 다른 노드로 넘어갈 때마다 절반의 경우의 수가 날아갈 경우 2^x = n 이므로 밑이 2인 로그 함수가 된다.
- 룩업, 삽입, 삭제 모두 O(log(n)) ~ O(n)이다.
- 트리 문제는 재귀적으로 푸는 능력을 본다.

``` c#
// 재귀적으로 풀 경우

Node findNode( Node root, int value ) {
  if ( root != null ) return null;
  int currval = root.getValue();
  if ( currval == value ) return root;
  if ( currval < value ) {
    return findNode( root.getRight(), value );
  } else {
    return findNode( root.getLeft(), value );
  }
}
```

<br/>

## 힙
- 노드의 각 자식의 값은 노드 자신의 값 이하여야 한다.
- 루트의 노드 값은 그 트리에서 가장 큰 값. 최댓값 구하기는 단지 루트를 리턴하면 됨. 최댓값을 빠르게 추출해야 한다면 힙을 사용하자.
- 룩업은 O(n), 삽입, 삭제는 O(log(n))

<br/>

## 일반적인 검색 방법
- 힙이나 이진트리가 아닌 다른 트리가 문제로 나오는 경우.
- 이 경우, 너비 우선 검색(BFS), 깊이 우선 검색(DFS)을 사용
  - 너비 우선 검색
    - 루트에서 시작하여 둘째 층을 왼쪽에서 오른쪽으로 훑어나감. 그 다음 충을 또 왼쪽에서 오른쪽으로 훑음. 
    - O(n)이고 어떤 층을 검색할 때 그 층에 있는 모든 노드의 자식 노드를 저장해둬야 하기 때문에 메모리 사용량이 높음. ***깊이 우선이랑 메모리차이 왜?***
    - 위 두가지 이유로 큰 트리에서 권장하는 방식은 아님.
  - 깊이 우선 검색
    - 가장 아래에 다다를때까지 쭉 내려가는 방식.
    - 아직 확인해보지 않은 자식이 있는 가장 가까운 조상 노드로 돌아가 검색을 계속 진행.
    - 각 층별로 모든 자식 노드를 저장할 필요가 없기 때문에 BFS에 비해 메모리 요구량이 적음.
    - 특정 층을 마지막으로 검색하는 문제가 없음.(BFS는 가장 낮은 층을 제일 늦게 확인하므로.)
    - 예를 들어 회사 조직도 트리에서 입사한지 3개월 미만인 직원을 찾는다면 BFS보단 DFS로 검색하면 더 빨리 찾을 수 있음.
  
<br />

## 종주
> 특정 노드를 찾으면 작업을 멈추는 검색과 달리 모든 노드를 방문하며 특정 작업을 수행해야 하는 경우 **종주**를 사용
- 프리오더 종주(preorder)
  - 노드 자체에 대해 어떤 작업을 수행하고 왼쪽 자손을 처리한 다음 오른쪽 자손을 처리. 항상 노드를 자식들보다 먼저 방문.
- 인오더 종주(inorder)
  - 우선 노드의 왼족 자손에 대해 작업 수행.
  - 왼쪽 서브 트리를 먼저 방문, 그 다음 노드 자체, 그 다음 오른쪽 서브 트리.
- 포스트오더 종주(postorder)
  - 노드의 왼쪽 자손에 대해 작업 수행 후 오른쪽 자손에 대해 작업 수행. 마지막으로 노드 그 자체에 대해 수행.
  - 모든 자식들을 자기 자신보다 항상 먼저 처리.

<br/>

## 그래프
- 트리와 달리 한 노드에 부모가 여럿일 수도 있어 루프(사이클)이 만들어질 수 있다.
- 노드 사이의 링크에도 가중치가 있을 수 있다.
- 가중치 등 별도의 정보를 담을 수 있는 링크를 **에지(edge)** 라고 함.  
<img src="https://user-images.githubusercontent.com/72545106/139589131-f6f22876-3775-40d0-a480-8e1256c3a3e5.png
"  alt="graph" width="300" />
  - 6-4 : 방향성 그래프 / 6-5 : 무방향성 그래프
  - 방향성 그래프 : ex) 도시를 연결하는 수로. A도시에서 D도시로 가장 빨리 물을 보낼 수 있는 경로를 구할 수 있음.
  - 무방향성 그래프 : 신호 전송에 쓰이는 일련의 릴레이.

- 구현방식
  - 인접 리스트(adjacency list) - 어떤 노드와 같은 에지를 공유하는 다른 노드에 대한 레퍼런스의 리스트
    - 한 노드에 연결되는 에지 개수에 제한이 없음. 
  - 노드 개수만큼의 차원 수로 만들어지는 정사각 행렬 형태의 자료구조로는 인접 행렬도 많이 쓰임. 
    - i, j 위치에 있는 행렬 원소가 i 노드에서 j노드로 이어지는 에지의 개수를 나타냄.

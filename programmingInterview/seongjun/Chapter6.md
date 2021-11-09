>프리오더 종주
>트리 높이
>케빈 베이컨 게임
>반복되지 않는 첫 번쨰 문자 찾기
>특정 문제 제거
>단어 뒤집기

# 트리와 그래프

## 트리

## 노드

```java
public abstract class Node{
	public Node[] children;
  public Node( Node[] children ){
    this.children = children;
  }
  public int getNumChildren(){
    return children.length;
  }
  public Node getChild(int index){
    return children[index];
  }
}
public class IntNode extends Node{
  public int value;
  public IntNode(Node[] children, int value){
    super(children);
    this.value = value;
  }
  public int getValue(){
    return value;
  }
}
```

## 이진트리

```java
public class Node{
	private Node left;
  private Node right;
  private int value;
  
  public Node( Node left, Node right, int value){
    this.left = left;
    this.right = right;
    this.value = value;
  }
  public Node getLeft(){ return left }
  public Node getRight(){ return right}
  public int getValue(){ return value }
}
```

* 트리 라고하면 이진트리인지 트리인지 분명히..

## 이진 검색 트리 Binary Search Tree

* bst를 그냥 트리로 부르는 경우도 흔함..
* 빠른 lookup 연산이 가능함 - 특정 노드의 위치 알아내기

```java
Node findNode( Node root, int value ){
	while(root !=null){
    int currval = root.getValue();
    if(currval == value) break;
    if(currval < value){
      root = root.getRight();
    }else{
      root = root.getLeft();
    }
  }
  return root
}
```

* 2^x = n - x 번 실행하면 ... n까지 찾을수있으니..
* x = log(n)
* 룩업이 log(n)
* 최악은 n  - 자식이 하나씩만
* 삭제, 삽입 연산도 log n
* 왼쪽만 따라가면 최소, 오른쪽만 따라가면 최대
* O n 으로 정렬된 순서로 출력 가능
* 어떤 노드 다음으로 높은 노드를 O log n시간안에 찾기가능
* 재귀적으로 생각할 수 있는 능력을 평가하기 위한 것들이 만핟....  - 트리의 각 노드는 그 노드에서 시작하는 서브트리의 노드이니..

```java
Node findNode( Node root, int value ){
	if(root !=null) return null;
  int currval = root.getValue();
  if(currval == value) break;
  if(currval < value){
    return findNode(root.getRight(), value);
  }else{
    return findNode(root.getLeft(), value);
  }
  return root
}
```

* 트리 관련은 재귀적으로 생각



## 힙

* 힙은 조금 특이한 형태의 트리

* 루트 노드값이 가장 큰/작은 값이고 상수시간으로 구할 수 있음

* 삽입 삭제는 여전히 log n 이고, 룩업은 O(n)임...
* BST처럼 주어진 노드 다음으로 큰 노드를 O logn으로 찾는다거나 n으로 정렬된 순서 출력 이런거 안됨

## 일반적인 검색 방법

* BST나 힙이 아닌 가계도나 직위체계등의 트리가 주어지는 경우가 있음...이럴땐 dfs, bfs

## 너비우선탐색

* Breadth First Search - 왼쪽에서 오른쪽으로 훑고... 
* 찾는거에 걸리는 시간은 n
* 모든 노드를 저장해야해서 메모리도 많이 씀

## 깊이 우선 탐색

* Depth First Search
* 끝에 다다를 떄 까지..
* 모든 자식 노드를 저장 할 필요가 없음
* 특정 층을 마지막으로 검색하는 문제가 발생하지 않음.
  * 찾고자하는 노드가 낮은 층에 있을거라고 예상되면 낮은층을 제일 늦게 검색하면 시간 마니걸리지?

## 종주

* traversal도 자주 나오는 문제 유형
* 특정 노드를 찾으면 멈추는게 아닌 각 노드를 종주하면서 어떤 작업을 수행
* preorder 종주 - 우선 노드 자체에 어떤 작업을 수행하고 왼쪽 자손을 처리하고 오른쪽자손을 처리 - 노드를 자식보다 먼저 방문
* inorder 종주 - 우선 노드의 왼쪽 자손 작업하고 노드 수행 오른쪽 수행
* postorder 종주 - 왼쪽 자손, 오른쪽 자손, 노드 수행

## 그래프

* 자식이 딸린 노드로 구성... 트리가 그래프의 한 종류죠?
* 단방향 - 방향성 그래프 / 양방향 - 무방향성 그래프 , 링크/엣지



# 문제

## 트리 높이

> 트리 높이는 루트 노드에서 잎 노드까지의 거리의 최댓값으로 정의된다. 
>
> 예를 들어 쟤는 4임, A에서 F G H까지 총 네 노드를 거치기 때문, 
>
> 임의의 이진 트리 높이를 계산하는 함수를 작성

![image](https://user-images.githubusercontent.com/72075148/139699746-d9d4aced-1b19-442c-a5bd-34774237823f.png)

* 일단 재귀적으로 풀 수 있는지 생각해본다, 각 노드는 그 노드를 루트로 하는 서브트리의 루트...

* 실행시간은 n임

* ```python
  def treeHeight(node):
    if(node == None): return 0;
    return 1 + max(treeHeight(node.left), treeHeight(node.right))
  ```

* 

## 프리오더 종주

> 프리오더 종주는 루트에서 시작해서 트리를 반시계 방향으로 돌면서 가장자리를 따라 움직이면서 만나게 되는 노드를 출력하는 방식으로 생각 가능
>
> 100, 50, 25, 75, 150, 125, 110, 175 순서대로 출력된다. 이진검색 트리에대해 프리오더 종주하면서 노드를 출력하라
>
> ![image](https://user-images.githubusercontent.com/72075148/139700739-c1c87a9b-1122-4b0c-8ef9-a8970302d00a.png)



```python
def preorder(node):
  if(node == None):
    return
  print(node.value)
  preorder(node.left)
  preorder(node.right)
```

## 재귀 안쓰는거

* 기본 개념 자체가 재귀적이므로,,, 재귀호출 자체는 호출 스택에 집어넣는 식으로. 스택구조를 쓴다.

```python
def preorder(node):
  queue = [node]
  while(queue.length > 0):
		n = queue.pop(0)
    print(n.value)
    if(n.left) queue.append(n.left)
    if(n.right) queue.append(n.right)
    
   	
  
```

n 임

## 케빈 베이컨 게임

> 케빈 베이컨 게임은 임의의 연기자와 케빈 베이컨을 연결하는 가장 짧은 경로를 찾는 게임
>
> 두 연기자가 같은 영화를 출연한적이 있으면 링크가 있는 것
>
> 어떤 연기자가 주어졌을 떄 그 연기자와 케빈 베이컨 사이를 가장 적은 수의 링크로 연결
>
> 모든 주류 영화 목록과 연기자 목록이 주어졌을 때 효율적으로 풀수있는 - 최소 링크ㄹ수를 ...

* 무방향성 그래프이다.

* 연기자를 노드로 만들고 영화를 엣지로 만든다..

* ```python
  def da(graph, first):
    queue = [[0, first]]
    distances = {inf}
    while(len(queue)>0):
      cur_distance, name = queue.pop(0)
      if(distances[name] < cur_distance):
        continue
       for a in graph[name]:
        distance = cur_dist + 1
        if distance < distances[name]:
          distances[name] = [distance, ]   
  ```
  
* 

* 






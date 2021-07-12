---
title: kick start 2021D
date: 2021-07-11 21:47:07
tags:
---



### [Arithmetic Square](https://codingcompetitions.withgoogle.com/kickstart/round/00000000004361e3/000000000082b813)

给一个3*3matrix，中间位置元素缺失，要求填上中间元素，使得矩阵中行、列、对角线形成的等差数列个数最多

枚举几种填数方式即可。

（唯一一道没WA的==)

```c
#include <bits/stdc++.h>
using namespace std;
#define int long long
#define sc(x) scanf("%lld",&(x));
#define pb push_back
#define fi first
#define se second
int A[3][3];
int t;
int check()
{
    int ans = 0;
    for(int i =0; i < 3; i++){
        if(2*A[i][1] == A[i][0]+A[i][2]){
            ans++;
        }
        if(2*A[1][i] == A[0][i]+A[2][i]){
            ans++;
        }
    }
    if(2*A[1][1] == A[0][0]+A[2][2])
        ans++;
    if(2*A[1][1] == A[0][2] + A[2][0])
        ans++;
    return ans;
}
int slove(){
    int x = A[0][0] + A[2][2];
    A[1][1] = x/2;
    int ans = 0;
    ans = check();
    x = A[2][0] + A[0][2];
    A[1][1] = x/2;
    ans = max(ans,check());
    x = A[1][0] + A[1][2];
    A[1][1] = x/2;
    ans = max(ans,check());
    x = A[0][1] + A[2][1];
    A[1][1] = x/2;
    ans = max(ans,check());
    return ans;
}
signed main(){
sc(t)
for(int i = 1; i <=t; i++){
    for(int i = 0; i < 3; i++){
        sc(A[0][i])
    }
    sc(A[1][0])sc(A[1][2])
    for(int i = 0; i < 3; i++){
        sc(A[2][i])
    }
    int ans = slove();
    cout << "Case #"<<i<<": "<<ans << '\n';
}
return 0;
}
```

<!--More-->

### [Cutting Intervals](https://codingcompetitions.withgoogle.com/kickstart/round/00000000004361e3/000000000082b933)

给一堆线段[$L_{i},R_{i}$],允许在选择C个整数点进行cut操作，一次在$K$点处的cut能把线段[$L,R$] (其中$L< K $,$K < R$),切成$[L,K]$,和$[K,R]$要求进行C次切割后得到的线段个数最多。

一个很朴素的想法就是贪心，从能切开最多线段的点开始。

注意到set 2给定的范围很大，所以枚举所有的整数点不现实。

容易看出的是一个点切割能产生新的线段数目在某些连续的区间内相等，只在线段的端点处发生着变化。

对端点进行枚举，记录端点处的变化情况。

```c
#include <bits/stdc++.h>
using namespace std;
#define int long long
#define sc(x) scanf("%lld",&(x));
#define pb push_back
#define fi first
#define se second
pair<int,int>P[100004];
set<int> st;
vector<int> vec;
int t;
int n;
//mp z记录的是分割能产生z条线段的端点数
map<int,int> mp;
vector<pair<int,int> > pv;
map<int,int> endW;
int C;
int slove()
{
    int ans = n;
    sort(P,P+n);
    for(int i = 0; i < n; i++)
    {
        st.insert(P[i].fi);
        st.insert(P[i].se);
        //记录一下这个点结尾的线段数目
        endW[P[i].se]+=1;
    }
    for(auto x: st)
    {
        vec.pb(x);
    }
    sort(vec.begin(),vec.end());
    int i = 0;
    int j = 0;
    int z = 0;
    int pre = vec[0];

    for(auto x : vec)
    {
        //前面一个区间[pre,x-1]都是的点分割都能产生z条线段
        if(x - pre > 1)
        mp[z] += x-pre-1;
        z-=endW[x];
        //当前点特殊处理?感觉实现有点丑了==
        mp[z] += 1;
        while(i<n &&P[i].fi == x){
            z++;i++;
        }
        pre = x;
    }

    for(auto x : mp){
        pv.pb(x);
    }
    //从大到小排序
    sort(pv.begin(),pv.end(),[=](const auto &x,const auto &y){
         return -x.fi < -y.fi;
         });
    //贪心
    for(auto w: pv){
        if(C > w.se){
            ans += w.se*w.fi;
            C-=w.se;
        }else{
            ans += C*w.fi;
            C = 0;
            break;
        }
    }
    st.clear();
    vec.clear();
    mp.clear();
    pv.clear();
    endW.clear();
    return ans;
}
signed main()
{
    sc(t)
    for(int i = 1; i <=t; i++)
    {
        sc(n)sc(C)

        for(int i = 0; i < n; i++)
        {
            sc(P[i].fi)sc(P[i].se)
        }
        int ans = slove();
        cout << "Case #"<<i<<": "<<ans << '\n';
    }
    return 0;
}
```

### [Final Exam](https://codingcompetitions.withgoogle.com/kickstart/round/00000000004361e3/000000000082bffc)

给一堆集合$[L_{i},L_{i}+1,\dots,R_{i}]$

给一个序列$[S_{1},S_{2},\dots,S_{n}]$

要求按照序列从左至右，从集合族中找一个元素$v$,满足$|v-S_{i}|$最小，如有多个元素满足要求，则选其中最小的。

一个元素在$i$位置被选择了，在后续的选择中不能再选它。

我们要求的操作有：

* 将$[L_{i},R_{i}]$中的元素加入集合。
* 从集合中选择与$S_{i}$最近的元素。
* 从集合中删除一个元素。

想法是用一个动态开点的线段树解决。

利用线段树可以很简单实现操作1，操作3.

至于操作2，我们可以维护一些信息，保证在值$S_{i}$的附近搜索。

动态开点：有需要时才给它建节点，1~$1e18$直接开不了。需要额外维护child信息，普通线段树child信息都是通过$2x+1$,$2x+2$形式得到的，但这里没有这种关系，所以需要一个数组来单独维护。至于每一个节点维护的范围，我们可以通过函数调用传参的时候记录，无需单独用数组记录，省一定的空间。

关于操作2,为了提高查询效率，我们需要在每个节点维护这个节点所包含的集合元素个数信息。某些不包含元素的节点就不用继续搜索。我们在查询时要进行一定规模剪枝。

当$S_{i}$ > 当前区间最大值，只需找到这个区间最小的元素。

当$S_{i}$ < 当前区间最小值，只需找到这个区间最大元素。

当$S_{i}$在当前区间的左子树的左子树，检查左子树的右子树是否有元素，有则只需要搜索左子树。

当$S_{i}$在当前区间的右子树的右子树，检查右子树的左子树是否有元素，有则只需要搜索右子树。

当$S_{i}$在当前区间的左子树，先搜索左子树，如果左子树最近的元素大于$S_{i}$，则不需检查右子树。

当$S_{i}$在当前区间的右子树，先搜索右子树，如果右子树最近的元素小于$S_{i}$，则无需检查左子树。

否则检查左右子树，找最小的。

注意懒标的上下传和动态开辟新点的处理。

```c
#include <bits/stdc++.h>
using namespace std;
#define int long long
#define sc(x) scanf("%lld",&(x));
#define pb push_back
#define fi first
#define se second
int t,n;
int x,y,q;
int maxn;
pair<int,int> P[100005];
int Q[100005];
//child信息
signed C[60000004][2];
//懒标
signed T[60000006];
//记录当前区间有多少个有效元素
signed D[60000006];

map<int,int> mp;
int k;
void init()
{

    C[1][0] = 0;
    C[1][1] = 0;
    D[1] = 0;
    T[1] = 0;
    k = 1;
}
void push_down(int x,int L,int R)
{
    int mid = (L + R)/2;
    if(C[x][0] == 0)
    {
        C[x][0] = ++k;
        C[C[x][0]][0] = C[C[x][0]][1] = 0;
        T[k]=0;
        D[k] = 0;
    }
    if(C[x][1] == 0)
    {
        C[x][1] = ++k;

        C[C[x][1]][0] = C[C[x][1]][1] = 0;

        T[k]=0;
        D[k] = 0;
    }
    D[C[x][0]]+= T[x]*(mid-L + 1);
    D[C[x][1]] += T[x]*(R-(mid+1) + 1);
    T[C[x][0]] += T[x];
    T[C[x][1]] += T[x];
    T[x] = 0;
}
void push_up(int x)
{
    D[x] = D[C[x][0]] + D[C[x][1]];
}
void add(int x,int l,int r,int L,int R)
{
   
int mid = (L + R)/2;

    if(L >= l && r >= R)
    {
        T[x] += 1;
        D[x] += R-L + 1;
        return;
    }
    push_down(x,L,R);
    if(l <= mid)
        add(C[x][0],l,r,L,mid);

    if(r > mid)

        add(C[x][1],l,r,mid+1,R);
    push_up(x);

}
void sub(int x,int v,int L,int R)
{
    int mid = (L + R)/2;

    if(L == v && R == v)
    {
        D[x]-=1;

        return;
    }
    push_down(x,L,R);
    if(v <= mid)
    {
        sub(C[x][0],v,L,mid);
    }
    else
    {
        sub(C[x][1],v,mid+1,R);
    }
    push_up(x);

}

int ask(int x,int v,int L,int R)
{
    int mid = (L + R)/2;
    if(D[x] == 0)return -1;

    int ans;
    if(L == R){
        return L;
    }
    push_down(x,L,R);
    if(v < L)
    {

        if(D[C[x][0]])
        {
            ans = ask(C[x][0],v,L,mid);
        }
        else
        {
            ans = ask(C[x][1],v,mid+1,R);
        }

    }
    else if(v > R)
    {
        if(D[C[x][1]])
        {
            ans = ask(C[x][1],v,mid+1,R);
        }
        else
        {
            ans = ask(C[x][0],v,L,mid);
        }

    }
    else if(v <= (L+mid)/2 && D[C[C[x][0]][1]]){
        ans = ask(C[x][0],v,L,mid);
    }else if(v > (mid+1+R)/2 && D[C[C[x][1]][0]]){
        ans = ask(C[x][1],v,mid+1,R);
    }
    else
    {
        int a=-1,b=-1;
        if(v <= mid){
        a = ask(C[x][0],v,L,mid);
        if(a == -1 || a < v)
        b = ask(C[x][1],v,mid+1,R);
        }
        if(v > mid){
            b = ask(C[x][1],v,mid+1,R);
            if(b == -1 || b > v)
                a = ask(C[x][0],v,L,mid);
        }
        if(a == -1)ans = b;
        else if(b == -1) ans = a;
        else if(abs(a-v) < abs(b-v))
        {
            ans = a;
        }
        else if(abs(a-v) == abs(b-v))
        {
            ans = min(a,b);
        }
        else
        {
            ans = b;
        }
    }
    push_up(x);
    return ans;
}
void slove()
{
    init();
    for(int i = 0; i < n; i++){
        add(1,P[i].fi,P[i].se,1,maxn);
    }
    for(int i = 0; i < q; i++){
        int v = ask(1,Q[i],1,maxn);
        sub(1,v,1,maxn);
        cout << v << ' ';
    }
    cout << '\n';


}
signed main()
{
    sc(t)
    for(int i = 1; i <=t; i++)
    {
        maxn = 0;
        sc(n)sc(q)
        for(int i = 0; i < n; i++)
        {
            sc(x)sc(y)
            P[i] = {x,y};
            maxn = max(maxn,y);
        }
        for(int i = 0; i < q; i++)
        {
            sc(Q[i])
        }
        cout << "Case #"<<i<<": ";
        slove();
    }
    return 0;
}

```

总结：

* 内存是真的不要钱，开8e7给过了==

### [Primes and Queries](https://codingcompetitions.withgoogle.com/kickstart/round/00000000004361e3/000000000082bcf4#problem)

只会set1，数据范围看错，第一个set WA到怀疑人生

```c
#include <bits/stdc++.h>
using namespace std;
#define int long long
#define sc(x) scanf("%lld",&(x));
#define pb push_back
#define fi first
#define se second
int t;
int n,Q,P;
int A[500005];
int S,L,R;
int V(int x)
{
    int ans = 0;
    if(x == 0)return 0;
    while(x%P == 0)
    {

        x/=P;
        ans++;
    }
    return ans;
}
int qp(int x,int n)
{
    int ans = 1;

    while(n)
    {
        if(n&1)
        {
            ans = ans * x;
        }
        n >>= 1;
        x = x*x;
    }
    return ans;
}
vector<int> vec;
int B[500004][5];
void add(int x,int v,int k){
    while(x <= 500000){
        B[x][k] += v;
        x += (x&-x);
    }
}
int ask(int x,int k){
    int ans = 0;
    while(x > 0){
        ans += B[x][k];
        x -= (x&-x);
    }
    return ans;
}
signed main()
{
    sc(t)
    int p;
    for(int i = 1; i <=t; i++)
    {
        memset(B,0,sizeof(B));
        sc(n)sc(Q)sc(P)
        for(int j = 1; j <= n; j++)
        {
            sc(A[j])
            for(int k = 1; k <= 4; k++){
                add(j,V(qp(A[j],k) - qp(A[j]%P,k)),k);
            }
        }

        int op;
        cout << "Case #"<<i<<": ";
        while(Q--)
        {
            sc(op)
            if(op ==1)
            {
                sc(p)
                for(int k = 1; k <= 4; k++){
                add(p,-V(qp(A[p],k) - qp(A[p]%P,k)),k);
            }
                sc(A[p])
                for(int k = 1; k <= 4; k++){
                add(p,V(qp(A[p],k) - qp(A[p]%P,k)),k);
            }

            }
            else
            {
                sc(S)sc(L)sc(R)
                cout <<ask(R,S) - ask(L-1,S)<<" ";
            }
        }
        
        cout << "\n";
        
    }
    return 0;
}


```


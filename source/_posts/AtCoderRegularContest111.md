---
title: AtCoder Regular Contest 111
date: 2021-01-09 22:20:47
tags: 题解
---
# [AtCoder Regular Contest 111](https://atcoder.jp/contests/arc111/tasks)

{% asset_img new-year-5798330__340.png %}

感觉BC写得有点复杂
## A - Simple Math 2
<!--More-->

```C++
#include <bits/stdc++.h>
 
using namespace std;
#define int long long
#define sc(x) scanf("%lld",&x);
#define pb push_back
#define fi first
#define se second
#define P pair<int,int>
int qp(int x, int y)
{
    int a = 10;
    int ans = 1;
    while(x){
        if(x&1){
            ans = (ans*a)%y;
        }
        a = (a*a)%y;
        x>>=1;
    }
    return ans;
}
signed main()
{
    int N;
    int M;
    sc(N) sc(M)
    cout <<qp(N,M*M)/M << '\n';
 
}
```

## B - Reversible Cards
```C++
#include <bits/stdc++.h>
 
using namespace std;
#define int long long
#define sc(x) scanf("%lld",&x);
#define pb push_back
#define fi first
#define se second
#define P pair<int,int>
set<int> sx,sy;
P A[200005];
queue<int> G[400005];
map<int,int>mp;
bool vis[400006];
bool f[200005];
signed main()
{
    int N;
    int x,y;
    sc(N)
    for(int i = 0; i < N; i++){
        sc(x)sc(y)
        A[i].fi = x;
        A[i].se = y;
        mp[x]+=1;
        mp[y] += 1;
        G[x].push(i);
        G[y].push(i);
    }
    priority_queue<P,vector<P>,greater<P> > pq;
    for(auto x: mp){
        pq.push({x.second,x.first});
    }
    int ans = 0;
    while(!pq.empty()){
        P a = pq.top();pq.pop();
        if(vis[a.second])continue;
        else {
            bool g = false;
            while(!G[a.second].empty()){
                int id = G[a.second].front();
                G[a.second].pop();
                if(!f[id]){
                    f[id] = true;
                    if(A[id].se != a.second){
                        mp[A[id].se] -= 1;
                        if(!vis[A[id].se])
                        pq.push({mp[A[id].se],A[id].se});
                    }else{
                        mp[A[id].fi] -= 1;
                        if(!vis[A[id].fi])
                        pq.push({mp[A[id].fi],A[id].fi});
                    }
                    g = true;
                    break;
                }
 
            }
            if(g)
            ans += 1;
            vis[a.second] = true;
 
        }
    }
    cout << ans << '\n';
 
}
```
## C - Too Heavy
```C++
#include <bits/stdc++.h>
 
using namespace std;
#define int long long
#define sc(x) scanf("%lld",&x);
#define pb push_back
#define fi first
#define se second
#define P pair<int,int>
int N;
int A[200005];
int B[200005];
int C[200005];
int fa[200005];
int dfs(int x)
{
    if(fa[C[x]])return x;
    fa[x] = -1;
    return min(x,dfs(C[x]));
}
void dfs1(int x,int y)
{
    fa[x] = y;
    if(fa[C[x]] == y)return;
    dfs1(C[x],y);
}
vector<int> G[200005];
signed main()
{
    sc(N)
    for(int i = 1; i <= N; i++)sc(A[i])
    for(int i = 1; i <= N; i++) sc(B[i])
    for(int i = 1; i <= N; i++)sc(C[i])
    if(N==1){
        printf("%d\n",0);
        return 0;
    }
    map<int,int> mp;
    for(int i = 1; i <= N; i++){
        if(A[i] <= B[C[i]]&&C[i]!=i){
            printf("%d\n",-1);
            return 0;
        }
        mp[B[C[i]]] = i;
    }
    for(int i = 1; i <= N; i++){
        if(C[i] == i)continue;
        if(fa[i])continue;
        int y = dfs(i);
        dfs1(i,y);
    }
    for(int i = 1; i <= N; i++){
        if(fa[i]){
            G[fa[i]].push_back(i);
        }
    }
    vector<P> ans;
    priority_queue<P> pq;
    for(int i = 1; i <= N; i++){
        if(G[i].size() > 0){
            while(!pq.empty())pq.pop();
            for(int x : G[i]){
                pq.push({B[x],x});
            }
            while(pq.size() > 1){
                P a = pq.top();pq.pop();
                int w = mp[a.first]; ///在哪？
                int v = a.second;///给谁
 
                C[w] = C[v];
                mp[B[C[w]]] = w;
                C[v] = v;
                ans.push_back({w,v});
            }
        }
    }
    cout << ans.size() << '\n';
    for(auto a : ans){
        cout << a.fi <<' ' << a.se << '\n';
    }
 
}
```
#include <iostream>
#include <cstdio>
#define MAXN 55
using namespace std;
int n,m;
int a[MAXN][MAXN];
int method[MAXN][MAXN];
int best_method[MAXN][MAXN];
int ans;
int able=0;
void dfs(int x,int y,int t);
int main(void){
    freopen("flip.in","r",stdin);
    freopen("flip.out","w",stdout);
    cin >> m >> n;
    for (int i=1;i<=m;i++)
        for (int j=1;j<=n;j++)
            cin >> a[i][j];
    ans=n*m+1;
    dfs(1,1,0);
    if (!able){
        cout << "IMPOSSIBLE\n";
        return 0;
    }
    int cnt=0;
    for (int i=1;i<=m;i++)
        for (int j=1;j<=n;j++)
            cnt+=best_method[i][j];
    cout << cnt << endl;
    for (int i=1;i<=m;i++){
        for (int j=1;j<=n;j++)
            cout << best_method[i][j] << ' ';
        cout << endl;
    }
    return 0;
}

void dfs(int x,int y,int t){
    if (t>=ans)
        return;
    if (x==m && y>n){
        for (int i=1;i<=n;i++)
            if (a[m][i])
                return;
        ans=t;
        able=1;
        for (int i=1;i<=m;i++)
            for (int j=1;j<=n;j++)
                best_method[i][j]=method[i][j];
        return;
    }
    if (y>n){
        dfs(x+1,1,t);
        return;
    }
    if (x==1){
        //Try not to reverse
        method[x][y]=0;
        dfs(x,y+1,t);
        
        //Try to reverse
        a[x][y]^=1;
        a[x][y+1]^=1;
        a[x][y-1]^=1;
        a[x+1][y]^=1;
        method[x][y]=1;
        dfs(x,y+1,t+1);
        a[x][y]^=1;
        a[x][y+1]^=1;
        a[x][y-1]^=1;
        a[x+1][y]^=1;
        return;
    }
    int res=a[x-1][y];
    a[x][y]^=res;
    a[x][y+1]^=res;
    a[x][y-1]^=res;
    a[x+1][y]^=res;
    method[x][y]=res;
    dfs(x,y+1,t+res);
    a[x][y]^=res;
    a[x][y+1]^=res;
    a[x][y-1]^=res;
    a[x+1][y]^=res;
}

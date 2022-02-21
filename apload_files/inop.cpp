#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

int main(){
    vector <vector<int>> g; // граф
    int n; // число вершин
    int s, tt; // стартовая вершина (вершины везде нумеруются с нуля)

    // чтение графа
    cin >> n;

    for(int i = 0; i < n; i++){
        g.push_back({});
        for(int j = 0; j < n; j++){
            int tmp; cin >> tmp;
            if(tmp == 1){
                g[i].push_back(j);
            }
        }
    }

    cin >> s >> tt;
    s--;
    tt--;

    queue<int> q;
    q.push (s);
    vector<bool> used (n);
    vector<int> d (n), p (n);
    used[s] = true;
    p[s] = -1;
    while (!q.empty()) {
        int v = q.front();
        q.pop();
        for (size_t i=0; i<g[v].size(); ++i) {
            int to = g[v][i];
            if (!used[to]) {
                used[to] = true;
                q.push (to);
                d[to] = d[v] + 1;
                p[to] = v;
            }
        }
    }

    if (!used[tt])
        cout << -1;
    else {
        vector<int> path;
        for (int v=tt; v!=-1; v=p[v])
            path.push_back (v);
        reverse (path.begin(), path.end());
        cout << d[tt] << endl;
        for (size_t i=0; i<path.size(); ++i)
            cout << path[i] + 1 << " ";
    }
}



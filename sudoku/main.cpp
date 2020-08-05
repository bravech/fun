#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>
#include <algorithm>
#include <utility>
#include <map>
#include <unordered_map>
#include <set>
#include <list>
#include <iterator>
#include <unordered_set>
#include <stack>
#include <queue>
#include <bitset>
#include <climits>
#include <string>
#include <sstream>
using namespace std;
 
typedef long long ll;
typedef pair<int, int> pii;
typedef pair<ll, int> pli;
typedef pair<ll, ll> pll;

const int MAXN = 100000 + 5, MAXB = 31;

int dx[9] = {-1, -1, -1, 0, 0, 0, 1, 1, 1}, dy[9] = {-1, 0, 1, -1, 0, 1, -1, 0, 1};

string grid = "";
vector<int> regions[11];
vector<pii> pairs[11];

bool mark[121], found_soln = false;
int row[11], col[11], maxr = -1, cnt = 0;

void search(int r) {
    if(r > maxr) {
        cout << r << endl;
        maxr = r;
    }
    if(r == 11) {
        cnt++;
        // not exactly 2 in row or column constraint
        for(int i = 0; i < 11; i++) {
            if(row[i] == 2 || col[i] == 2)
                return;
        }
        // found solution
        found_soln = true;
        for(int i = 0; i < 11; i++) {
            for(int j = 0; j < 11; j++) {
                cout << mark[i * 11 + j];
            }
            cout << endl;
        }
        return;
    }

    int rnum = 0, cnum = 0, rnum2 = 0, cnum2 = 0;
    for(int i = 0; i < 11; i++) {
        rnum += (row[i] == 0);
        cnum += (col[i] == 0);
        rnum2 += (row[i] == 2);
        cnum2 += (col[i] == 2);
    }

    int moves_left = 2 * (11 - r);
    // at least one per row and column
    if(rnum > moves_left || cnum > moves_left) return;
    // not exactly 2 in row or column constraint
    if(rnum2 > moves_left || cnum2 > moves_left) return;

    for(int k = 0; k < pairs[r].size(); k++) {
        pii p = pairs[r][k];
        bool works = true;
        // touching constraint
        for(int i = 0; i < 9; i++) {
            int nx = (p.first / 11) + dx[i], ny = (p.first % 11) + dy[i];
            if(nx >= 0 && nx < 11 && ny >= 0 && ny < 11 && mark[nx * 11 + ny]) {
                works = false;
                break;
            }
            nx = (p.second / 11) + dx[i], ny = (p.second % 11) + dy[i];
            if(nx >= 0 && nx < 11 && ny >= 0 && ny < 11 && mark[nx * 11 + ny]) {
                works = false;
                break;
            }
        }
        if(works) {
            mark[p.first] = mark[p.second] = true;
            row[p.first / 11]++, row[p.second / 11]++;
            col[p.first % 11]++, col[p.second % 11]++;
            search(r + 1);
            if(found_soln) return;
            mark[p.first] = mark[p.second] = false;
            row[p.first / 11]--, row[p.second / 11]--;
            col[p.first % 11]--, col[p.second % 11]--;
        }
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    for(int i = 0; i < 11; i++) {
        string s;
        cin >> s;
        grid += s;
    }
    for(int i = 0; i < grid.length(); i++) {
        regions[grid[i] - 'a'].push_back(i);
    }

    for(int k = 0; k < 11; k++) {
        for(int i = 0; i < regions[k].size(); i++) {
            for(int j = i + 1; j < regions[k].size(); j++) {
                int a = regions[k][i], b = regions[k][j];
                // touching constrint
                if(abs(a / 11 - b / 11) <= 1 && abs(a % 11 - b % 11) <= 1) continue;
                pairs[k].push_back(make_pair(a, b));
            }
        }
    }

    for(int i = 0; i < 11; i++) {
        row[i] = col[i] = 0;
        for(int j = 0; j < 11; j++) {
            mark[i * 11 + j] = false;
        }
    }

    search(0);
    cout << cnt << endl;
    return 0;
} 
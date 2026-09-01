#include <stdio.h>

int main() {
    int a[10][10];
    int r, c;

    for (r = 0; r < 10; r++) {
        for (c = 0; c < 10; c++) {
            if (scanf("%d", &a[r][c]) != 1) return 0;
        }
    }

    if (a[0][0] == 1 || a[9][9] == 1) {
        printf("-1");
        return 0;
    }

    int pr[10][10], pc[10][10];
    for (r = 0; r < 10; r++) {
        for (c = 0; c < 10; c++) {
            pr[r][c] = -1;
            pc[r][c] = -1;
        }
    }

    int qr[100], qc[100];
    int head = 0, tail = 0;

    pr[0][0] = 0;
    pc[0][0] = 0;
    qr[tail] = 0;
    qc[tail] = 0;
    tail++;

    int dr[4] = {1, 0, -1, 0};
    int dc[4] = {0, 1, 0, -1};

    while (head < tail) {
        int x = qr[head], y = qc[head];
        head++;

        if (x == 9 && y == 9) break;

        for (int d = 0; d < 4; d++) {
            int nx = x + dr[d];
            int ny = y + dc[d];
            if (nx >= 0 && nx < 10 && ny >= 0 && ny < 10) {
                if (a[nx][ny] == 0 && pr[nx][ny] == -1) {
                    pr[nx][ny] = x;
                    pc[nx][ny] = y;
                    qr[tail] = nx;
                    qc[tail] = ny;
                    tail++;
                }
            }
        }
    }

    if (pr[9][9] == -1) {
        printf("-1");
        return 0;
    }

    int pathr[100], pathc[100], len = 0;
    int x = 9, y = 9;

    while (!(x == 0 && y == 0)) {
        pathr[len] = x;
        pathc[len] = y;
        len++;
        int nx = pr[x][y];
        int ny = pc[x][y];
        x = nx;
        y = ny;
    }

    pathr[len] = 0;
    pathc[len] = 0;
    len++;

    for (int i = len - 1; i >= 0; i--) {
        if (i != 0) printf("(%d,%d), ", pathr[i] + 1, pathc[i] + 1);
        else printf("(%d,%d)", pathr[i] + 1, pathc[i] + 1);
    }

    return 0;
}

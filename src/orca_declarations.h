#ifndef ORCA_DECLARATIONS_H
#define ORCA_DECLARATIONS_H

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cassert>
#include <ctime>
#include <iostream>
#include <fstream>
#include <set>
#include <unordered_map>
#include <algorithm>

using namespace std;

typedef long long int64;
typedef pair<int, int> PII;
typedef struct
{
    int first, second, third;
} TIII;

typedef PII PAIR;
typedef TIII TRIPLE;

// Function declarations only
extern int n, m;
extern int *deg;
extern PAIR *edges;
extern int **adj;
extern int *adj_matrix;
extern bool (*adjacent)(int, int);
extern int64 **orbit;
extern int64 **eorbit;

// Function declarations
bool operator<(const PAIR &x, const PAIR &y);
bool operator==(const PAIR &x, const PAIR &y);
bool operator<(const TRIPLE &x, const TRIPLE &y);
bool operator==(const TRIPLE &x, const TRIPLE &y);

bool adjacent_list(int x, int y);
bool adjacent_matrix(int x, int y);
int getEdgeId(int x, int y);

void count4();
void ecount4();
void count5();
void ecount5();

// Main interface functions
int motif_counts(const char *orbit_type, int graphlet_size,
                 const char *input_filename, const char *output_filename, std::string &out_str);

int motif_counts(char *orbit_type, int graphlet_size,
                 const char *input_filename, const char *output_filename);

#endif // ORCA_DECLARATIONS_H

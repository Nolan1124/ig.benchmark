/* -*- mode: C; mode: folding; fill-column: 70; -*- */
/* Copyright 2010,  Georgia Institute of Technology, USA. */
/* See COPYING for license. */
#include "compat.h"
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <math.h>

#include <assert.h>

#include <alloca.h> /* Portable enough... */
#include <fcntl.h>
#include <unistd.h>

#if !defined(__MTA__)
#include <getopt.h>
#endif


#include "graph500.h"
#include "rmat.h"
#include "kronecker.h"
#include "verify.h"
#include "prng.h"
#include "xalloc.h"
#include "options.h"
#include "generator/splittable_mrg.h"
#include "generator/make_graph.h"


static int64_t nvtx_scale;

static struct packed_edge * restrict IJ;
static int64_t nedge;

static int64_t bfs_root[NBFS_max];

int
main (int argc, char **argv)
{
  int * restrict has_adj;
  FILE* fd;
  FILE* fd2;
  int64_t desired_nedge;
  if (sizeof (int64_t) < 8) {
    fprintf (stderr, "No 64-bit support.\n");
    return EXIT_FAILURE;
  }

  if (argc > 1)
    get_options (argc, argv);

  nvtx_scale = 1L<<SCALE;

  init_random ();

  desired_nedge = nvtx_scale * edgefactor;
  /* Catch a few possible overflows. */
  assert (desired_nedge >= nvtx_scale);
  assert (desired_nedge >= edgefactor);


  fprintf (stderr, "Generating edge list... (nedges:%d) (scale:%d)\n",desired_nedge,SCALE);
  if (use_RMAT) {
      fprintf(stderr,"Using rmat\n");
      nedge = desired_nedge;
      IJ = xmalloc_large_ext (nedge * sizeof (*IJ));
      rmat_edgelist (IJ, nedge, SCALE, A, B, C);
  }
  else {
      fprintf(stderr,"Using make_graph\n");
      make_graph(SCALE, desired_nedge, userseed, userseed, &nedge, (struct packed_edge**)(&IJ));
  }
  if (VERBOSE) fprintf (stderr, " done.\n");

  if (dumpname){
      fd2 = fopen (dumpname, "w");//O_WRONLY|O_CREAT|O_TRUNC, 0666);
      fprintf(stderr,"Opening file %s (%d)\n",dumpname,fd2);
  }
  else
    fd2 = 0;

  if (fd2 == 0) {
    fprintf (stderr, "Cannot open output file : %s\n",
	     (dumpname? dumpname : "stdout"));
    return EXIT_FAILURE;
  }


  /*
  fprintf(stderr,"Writing edges (%p) (%d) \n",IJ,(2*nedge*sizeof(*IJ)));
  s = write (fd, IJ, 2 * nedge * sizeof (*IJ));
  fprintf(stderr,"Wrote (%d)\n",s);
  */
 


  fprintf(stderr,"Writing fstream  edges (%p) (%d) \n",IJ,(2*nedge*sizeof(*IJ)));
//  s = fwrite (IJ,2 * nedge * sizeof (*IJ),1,fd2);
  {
      int i = 0;
      for(i = 0;i < nedge;i++ )
      {
          fprintf(fd2,"%d,%d\n",IJ[i].v0,IJ[i].v1);
      }
  }


  
  fclose (fd2);
 
  char buffer[] = "test.text";
  if(!rootname){
      rootname = buffer;
  }
  fprintf(stderr,"Root name=(%s) dumpname=(%s)\n",rootname,dumpname);
  fd = fopen (rootname,"w"); //O_WRONLY|O_CREAT|O_TRUNC, 0666);
  

  
  if (rootname >= 0) {
    has_adj = xmalloc_large (nvtx_scale * sizeof (*has_adj));
    OMP("omp parallel") {
      OMP("omp for")
	for (int64_t k = 0; k < nvtx_scale; ++k)
	  has_adj[k] = 0;
      MTA("mta assert nodep") OMP("omp for")
	for (int64_t k = 0; k < nedge; ++k) {
	  const int64_t i = get_v0_from_edge(&IJ[k]);
	  const int64_t j = get_v1_from_edge(&IJ[k]);
	  if (i != j)
	    has_adj[i] = has_adj[j] = 1;
	}
    }

    /* Sample from {0, ..., nvtx_scale-1} without replacement. */
    {
      int m = 0;
      int64_t t = 0;
      while (m < NBFS && t < nvtx_scale) {
	double R = mrg_get_double_orig (prng_state);
	if (!has_adj[t] || (nvtx_scale - t)*R > NBFS - m) ++t;
	else {
            bfs_root[m++] = t++;
//            fprintf(stderr,"bfs[%d] = %d\n",m-1,bfs_root[m-1]);
        }
      }
      if (t >= nvtx_scale && m < NBFS) {
	if (m > 0) {
	  fprintf (stderr, "Cannot find %d sample roots of non-self degree > 0, using %d.\n",
		   NBFS, m);
	  NBFS = m;
	} else {
	  fprintf (stderr, "Cannot find any sample roots of non-self degree > 0.\n");
	  exit (EXIT_FAILURE);
	}
      }
    }

    xfree_large (has_adj);
    fprintf(stderr,"Root size %d\n",NBFS*sizeof (*bfs_root));
    //write (fd, bfs_root, NBFS * sizeof (*bfs_root));
    {
        int i;
        for(i = 0;i < NBFS_max; i++)
        {
            fprintf(fd,"%d\n",bfs_root[i]);
        }
    }
    
    fclose (fd);
    
  }

  return EXIT_SUCCESS;
}

////////////////////////////////////////////////////////////////////////////////
//
// Copyright (c) 2008 The Regents of the University of California
//
// This file is part of Qbox
//
// Qbox is distributed under the terms of the GNU General Public License
// as published by the Free Software Foundation, either version 2 of
// the License, or (at your option) any later version.
// See the file COPYING in the root directory of this distribution
// or <http://www.gnu.org/licenses/>.
//
////////////////////////////////////////////////////////////////////////////////
//
// CellMass.h
//
////////////////////////////////////////////////////////////////////////////////
// $Id: CellMass.h,v 1.4 2008-09-08 15:56:18 fgygi Exp $

#ifndef CELLMASS_H
#define CELLMASS_H

#include<iostream>
#include<iomanip>
#include<sstream>
#include<stdlib.h>

#include "Sample.h"

class CellMass : public Var
{
  Sample *s;

  public:

  char *name ( void ) const { return "cell_mass"; };

  int set ( int argc, char **argv )
  {
    if ( argc != 2 )
    {
      if ( ui->onpe0() )
      cout << " cell_mass takes only one value" << endl;
      return 1;
    }

    double v = atof(argv[1]);
    if ( v <= 0.0 )
    {
      if ( ui->onpe0() )
        cout << " cell_mass must be positive" << endl;
      return 1;
    }

    s->ctrl.cell_mass = v;
    return 0;
  }

  string print (void) const
  {
     ostringstream st;
     st.setf(ios::left,ios::adjustfield);
     st << setw(10) << name() << " = ";
     st.setf(ios::right,ios::adjustfield);
     st << setw(10) << s->ctrl.cell_mass;
     return st.str();
  }

  CellMass(Sample *sample) : s(sample) { s->ctrl.cell_mass = 10000.0; }
};
#endif

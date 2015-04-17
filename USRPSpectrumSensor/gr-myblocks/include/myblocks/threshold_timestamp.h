/* -*- c++ -*- */
/* 
 * Copyright 2015 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */


#ifndef INCLUDED_MYBLOCKS_THRESHOLD_TIMESTAMP_H
#define INCLUDED_MYBLOCKS_THRESHOLD_TIMESTAMP_H

#include <myblocks/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace myblocks {

    /*!
     * \brief <+description of block+>
     * \ingroup myblocks
     *
     */
    class MYBLOCKS_API threshold_timestamp : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<threshold_timestamp> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of myblocks::threshold_timestamp.
       *
       * To avoid accidental use of raw pointers, myblocks::threshold_timestamp's
       * constructor is in a private implementation
       * class. myblocks::threshold_timestamp::make is the public interface for
       * creating new instances.
       */
      static sptr make(unsigned int vlen, size_t itemsize, int type, float threshold, int fd);
    };

  } // namespace myblocks
} // namespace gr

#endif /* INCLUDED_MYBLOCKS_THRESHOLD_TIMESTAMP_H */

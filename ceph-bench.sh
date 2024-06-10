#!/bin/bash

# Function to run ceph osd bench and parse bytes_per_sec
run_ceph_osd_bench() {
  local osd_id=$1
  output=$(ceph tell osd.$osd_id bench 2>&1)
  if [ $? -eq 0 ]; then
    bytes_per_sec=$(echo "$output" | grep -oP '"bytes_per_sec": \K[0-9.]+')
    echo "$osd_id: $bytes_per_sec"
  else
    echo "Failed to run ceph osd bench for osd.$osd_id. Error:" >&2
    echo "$output" >&2
  fi
}

# Function to sort results by bytes_per_sec
sort_results() {
  local results=("$@")
  printf "%s\n" "${results[@]}" | sort -t ':' -k2 -n
}

# Main script
main() {
  local osd_id_start="$1"
  local osd_id_end="$2"
  local results=()

  if [ -z "$osd_id_start" ] || [ -z "$osd_id_end" ]; then
    echo "Usage: $0 <osd_id_start> <osd_id_end>"
    exit 1
  fi

  for (( osd_id=osd_id_start; osd_id<=osd_id_end; osd_id++ )); do
    osd_result=$(run_ceph_osd_bench "$osd_id")
    results+=("$osd_result")
  done

  sorted_results=$(sort_results "${results[@]}")

  # Write output to file with timestamp
  timestamp=$(date +"%Y%m%d_%H%M%S")
  output_file="ceph_osd_bench_results_$timestamp.txt"
  printf "%s\n" "$sorted_results" > "$output_file"
  echo "Results written to $output_file"
}

main "$@"

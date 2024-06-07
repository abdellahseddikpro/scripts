#!/bin/bash

# Function to run ceph osd bench and parse IOPS
run_ceph_osd_bench() {
  local osd_id=$1
  local runs=$2
  local results=()

  for (( run=1; run<=runs; run++ )); do
    echo "Running ceph osd bench test $run for osd.$osd_id..."
    output=$(ceph tell osd.$osd_id bench 2>&1)
    if [ $? -eq 0 ]; then
      echo "Output for run $run:"
      echo "$output"
      iops=$(echo "$output" | grep -oP '"iops": \K[0-9.]+')
      results+=("$osd_id: $iops")
    else
      echo "Failed to run ceph osd bench for osd.$osd_id on run $run. Error:"
      echo "$output"
    fi
  done

  echo "${results[@]}"
}

# Function to sort results by IOPS
sort_results() {
  local results=("$@")
  printf "%s\n" "${results[@]}" | sort -t ':' -k2 -n
}

# Main script
main() {
  local osd_id="$1"
  local runs="${2:-1}"
  local results=()

  if [ -z "$osd_id" ]; then
    echo "Usage: $0 <osd_id> [runs]"
    exit 1
  fi

  results=($(run_ceph_osd_bench "$osd_id" "$runs"))
  sorted_results=$(sort_results "${results[@]}")

  echo "Sorted results by IOPS:"
  printf "%s\n" "$sorted_results"

  # Write output to file with timestamp
  timestamp=$(date +"%Y%m%d_%H%M%S")
  output_file="ceph_osd_bench_results_$timestamp.txt"
  printf "%s\n" "$sorted_results" > "$output_file"
  echo "Results written to $output_file"
}

main "$@"

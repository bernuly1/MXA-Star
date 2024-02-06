import gc
import time

from a_star import a_star
# from corner_search_new import corner_search_new
from perfect_runner import p_a_star_runner
from perfect_runner_turbo import p_a_star_turbo
import sensing_a_star
from sensing_perfect_runner import sensing_perfect_a_star
#from octile.octile_a_star import octile_a_star as corner_search
#from octile.octile_a_star_sensing import octile_a_star_sensing as corner_search
#from octile.perfect_runner_octile import perfect_runner_octile as corner_search
#from octile.perfect_sensing_runner_octile import perfect_sensing_runner_octile as corner_search
from g_node_3 import g_node
from map_reader import map_reader


def get_coordinates(coordinates_str):
    coordinates_arr = [int(x.strip()) for x in coordinates_str.strip()[1:-1].split(",")]
    stat_node = g_node((coordinates_arr[1], coordinates_arr[0]))
    goal_node = g_node((coordinates_arr[3], coordinates_arr[2]))
    return stat_node, goal_node


def read_input(instances_file):
    ret = []
    for line in instances_file:
        start_node, goal_node = get_coordinates(line)
        ret.append((start_node, goal_node))

    return ret


def get_corner_search(map_reader, algorithm):

    if algorithm == 0:
        return a_star(map_reader)
    elif algorithm == 1:
        return sensing_a_star.a_star(map_reader)
    elif algorithm == 2:
        return p_a_star_runner(map_reader)
    elif algorithm == 3:
        return sensing_perfect_a_star(map_reader)




if __name__ == "__main__":
    import pathlib
    import re
    import argparse
    parser = argparse.ArgumentParser(
        description="CLO algorithm, best algorithm for grids",
        prog="corner_search",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "input_path",
        metavar="INPUT_PATH",
        type=pathlib.Path,
        help="Input problem instances file path. "
    )
    parser.add_argument("--map-path", type=pathlib.Path,
                        help="The path to the .map file")
    parser.add_argument("--first", type=int, default=0, help="Index of the first instance to solve")
    parser.add_argument("--last", type=int, default=-1, help="Index of the last instance to solve")
    parser.add_argument("--algorithm", type=int, default=0, help="which algorithm to use")
    parser.add_argument("--out-file", type=str, default="", help="file name to write the solution")


    args = parser.parse_args()
    try:
        print(args.input_path)
        path = pathlib.PurePath(args.input_path)
        map_reader = map_reader()
        map_reader.create_map(args.map_path)

    except Exception as e:
        raise Exception("There must be a directory with the grid name, brc203d, spiral, etc... ") from e
    with open(args.input_path) as f:
        start_goal_states = read_input(f)
    for i, start_goal_state in enumerate(start_goal_states):
        if i < args.first:
            continue
        #if i % 15 != 0:
        #    continue
        if 0 <= args.last < i:
            break
        # print(f"Solving instance {i}: ", end="", flush=True)

        run_a_star = get_corner_search(map_reader, args.algorithm)
        start_time = time.time()
        search_path = run_a_star.search(start_goal_state[0], start_goal_state[1])
        end_time = time.time() - start_time
        run_time = round(end_time, 3)
        map_path = pathlib.PurePath(args.map_path)
        map_name = map_path.name.replace(".map", "")
        jason_dict = {"instance": i, "map": map_name, "s_x": start_goal_state[0].position[0],
                      "s_y": start_goal_state[0].position[1], "g_x": start_goal_state[1].position[0],
                      "g_y": start_goal_state[1].position[1], "cost": search_path[-1].g, "time": run_time,
                      "generated": run_a_star.count_generated, "expanded": run_a_star.count_expanded,
                      "lazy_switch": run_a_star.lazy_switch, "walls_added": run_a_star.count_wall,
                      "start_h": run_a_star.start_h, "local_generated": run_a_star.local_generated,
                      "local_expanded": run_a_star.local_expanded, "local_walls": run_a_star.local_walls,
                      "sensing": len(run_a_star.sensing), "algorithm": args.algorithm}


        with open(args.out_file, 'w') as f:
            f.write(jason_dict)
        print(f"solved {args.algorithm}", flush=True)
        # print(jason_dict, flush=True)
        jason_dict = None
        run_a_star.map_reader = None
        del run_a_star
        run_a_star = None
        gc.collect()
        exit()




        # print(f"solved with cost {len(search_path)} in {end_time:.3f} seconds"
        #       f"{run_a_star.count_generated} nodes generated "
        #       f"{run_a_star.count_expanded} nodes expanded "
        #       f"{run_a_star.lazy_switch} times did a lazy switch "
        #       f"{run_a_star.count_wall} walls added "
        #       )



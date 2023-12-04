use std::fs;
use std::collections::HashSet;

fn valid_round(round: &str) -> bool {
    let parts: Vec<&str> = round.split(",").collect();
    for part in parts {
        let (count, colour) = part.trim().split_once(" ").unwrap();
        let count: i32 = count.trim().parse().unwrap();
        let colour = colour.trim();
        if colour == "red" && count > 12 {
            return false;
        } else if colour == "blue" && count > 14 {
            return false;
        }
        else if colour == "green" && count > 13 {
            return false;
        }
    }
    println!("{round} is valid");
    return true;
}

fn valid_game(game: &str) -> bool {
    println!("Game: {game}");
    let rounds:Vec<&str> = game.split(";").collect();
    for round in rounds {
        if !valid_round(round) {
            return false;
        }
    }
    return true;
}

fn main() {
    let file_contents = fs::read_to_string("input.txt").expect("Failed to read file");
    let lines: Vec<String> = file_contents.lines().map(|line| line.to_string()).collect();
    let mut valid_games: HashSet<i32> = HashSet::new();
    for line in lines {
        let (game_id, game) = line.split_once(":").unwrap();
        let (_, game_num) = game_id.split_once(" ").unwrap();
        let game_num: i32 = game_num.parse().unwrap();

        if valid_game(game) {
            valid_games.insert(game_num);
        }
    }
    
    let sum: i32 = valid_games.iter().sum();
    println!("Sum of valid games: {}", sum);
}
import {KeyValueItem} from "./KeyValueItem";

export interface Movie {
  pk: number;
  movie_title: string;
  genres: KeyValueItem[];
  released: string;
  runtime: number;
  black_and_white: boolean;
  country?: KeyValueItem;
  rating:number;
}

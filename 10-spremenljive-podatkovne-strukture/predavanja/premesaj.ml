let zamenjaj tabela i j =
  let t = tabela.(i) in
  tabela.(i) <- tabela.(j);
  tabela.(j) <- t

let ne_na_mestu f_na_mestu tabela =
  let kopija = Array.copy tabela in
  let () = f_na_mestu kopija in
  kopija

let obrni_na_mestu tabela =
  let n = Array.length tabela in
  for i = 0 to n / 2 - 1 do
    zamenjaj tabela i (n - i - 1)
  done

let obrni tabela =
  let n = Array.length tabela in
  Array.init n (fun i -> tabela.(n - i - 1))

let obrni' tabela =
  ne_na_mestu obrni_na_mestu tabela

let fisher_yates_na_mestu tabela =
  let n = Array.length tabela in
  for i = n - 1 downto 1 do
    let j = Random.int (i + 1) in
    zamenjaj tabela i j
  done

let fisher_yates tabela =
  ne_na_mestu fisher_yates_na_mestu tabela

let urejena_tabela n =
  Array.init n (fun i -> i + 1)

let prikazi_verjetnosti verjetnosti =
  let urejene_verjetnosti =
    List.sort (fun (_, p1) (_, p2) -> -compare p1 p2) verjetnosti
  in
  match urejene_verjetnosti with
  | [] -> ()
  | (_, max_p) :: _ ->
      let max_sirina = 50 in
      urejene_verjetnosti
      |> List.iter (fun (x, p) ->
          let sirina =
            int_of_float (float_of_int max_sirina *. p /. max_p)
          in
          let stolpec =
            String.make sirina '='
            ^ String.make (max_sirina - sirina) ' '
          in
          Format.printf "%s %s (%f%%)\n" x stolpec (100. *. p)
      )

let verjetnost_rezultatov poskus stevilo_poskusov =
  let ponovitve = Hashtbl.create 256 in
  for _ = 1 to stevilo_poskusov do
    let rezultat = poskus () in
    if Hashtbl.mem ponovitve rezultat then
      Hashtbl.replace ponovitve rezultat (Hashtbl.find ponovitve rezultat + 1)
    else
      Hashtbl.add ponovitve rezultat 1
  done;
  Hashtbl.fold (fun rezultat stevilo seznam ->
    (rezultat, float_of_int stevilo /. float_of_int stevilo_poskusov) :: seznam
  ) ponovitve []

let verjetnost_permutacij premesaj stevilo_poskusov velikost_permutacije =
  let tabela = Array.init velikost_permutacije (fun i -> string_of_int (i + 1)) in
  let poskus () =
    tabela
    |> premesaj
    |> Array.to_list
    |> String.concat ""
  in
  verjetnost_rezultatov poskus stevilo_poskusov
  |> prikazi_verjetnosti

let fiksne_tocke premesaj tabela =
  let tabela' = premesaj tabela in
  let isti = ref 0 in
  for i = 0 to Array.length tabela - 1 do
    if tabela.(i) = tabela'.(i) then incr isti
  done;
  !isti

;;

Random.self_init ();
verjetnost_permutacij fisher_yates 50000 4
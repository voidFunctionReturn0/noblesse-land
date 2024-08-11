defmodule Service.Point do
  @behaviour Ecto.Type

  def type, do: :point

  # DB에 저장할 때의 변환
  def cast({x, y} = point) when is_float(x) and is_float(y), do: {:ok, point}
  def cast(_), do: :error

  # DB에서 데이터 로드할 때의 변환
  def load(%Postgrex.Point{x: x, y: y}), do: {:ok, {x, y}}
  def load(_), do: :error

  # DB에 저장할 때의 덤프
  def dump({x, y} = _point) when is_float(x) and is_float(y), do: {:ok, %Postgrex.Point{x: x, y: x}}
  def dump(_), do: :error

  # Ecto에서 데이터를 임베드할 때의 변환(nil 반환을 기본 동작으로 사용)
  def embed_as(_format), do: :self

  # Point 동일한지 비교
  def equal?({x1, y1}, {x2, y2}), do: x1 == x2 and y1 == y2
  def equal?(_, _), do: false
end
